import mcp.types as types
import FreeCAD
import json
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue, Object
from rpc_server.serialize import serialize_object

tool_type = types.Tool(
                name="Part-Extrusion",
                description="Create a named extrude object in a named document",
                inputSchema={
                    "type": "object",
                    "required": ["DocName", "ObjName"],
                    "properties": {
                        "DocName": {
                            "type": "string",
                            "description": "Name of document in which to create",
                        },
                        "ObjName": {
                            "type": "string",
                            "description": "Name of object to create",
                        },
                        "Properties": {
                            "BaseName": {
                                "type": "string",
                                "description": "Name of base object shape"
                            }, 
                            "DirMode": {
                                "type": "string",
                                "description": "Normal, Edge or Custom."
                            }, 
                            "Dir": {
                                "X": {
                                    "type": "number",
                                    "description": "X component of direction"
                                },
                                "Y": {
                                    "type": "number",
                                    "description": "Y component of direction"
                                },
                                "Z": {
                                    "type": "number",
                                    "description": "Z component of direction"
                                }
                            }, 
                            "DirLink": {
                                "type": "string",
                                "description": "Link to object for Normal or Edge DirMode"
                            }, 
                            "LengthFwd": {
                                "type": "number",
                                "description": "Length to extrude forward"
                            }, 
                            "LengthRev": {
                                "type": "number",
                                "description": "Length to extrude reverse"
                            }, 
                            "Solid": {
                                "type": "boolean",
                                "description": "Create solid"
                            }, 
                            "Reversed": {
                                "type": "boolean",
                                "description": "Direction reversed"
                            }, 
                            "Symmetric": {
                                "type": "boolean",
                                "description": "Extrude symmetric"
                            }, 
                            "TaperAngle": {
                                "type": "number",
                                "description": "Taper angle forward"
                            }, 
                            "TaperAngleRev": {
                                "type": "number",
                                "description": "Taper angle reverse"
                            }, 
                        },
                    },
                },
            )

def do_it(args):
    doc_name = args.get("DocName")
    probj = Object(
        name=args.get("ObjName", "Extrusion"),
        type="Part::Extrusion",
        analysis=args.get("Analysis", None),
        properties=args.get("Properties", {}),
    )
    rpc_request_queue.put(lambda: _extrude_shape_gui(doc_name, probj))
    res, text = rpc_response_queue.get()
    return [types.TextContent(type="text", text=text)]

def _extrude_shape_gui(doc_name, probj):
    doc = FreeCAD.getDocument(doc_name)
    if not doc:
        FreeCAD.Console.PrintError(f"Document '{doc_name}' not found.\n")
        return False, f"Document '{doc_name}' not found.\n"
    try:
        obj = doc.addObject(probj.type, probj.name)
        obj.Base = doc.getObject(probj.properties["Base"])
        obj.DirMode = probj.properties["DirMode"]
        obj.DirLink = doc.getObject(probj.properties["DirLink"])
        obj.Dir = FreeCAD.Vector(probj.properties["Dir"]["X"], probj.properties["Dir"]["Y"], probj.properties["Dir"]["Z"])
        obj.LengthFwd = float(probj.properties["LengthFwd"])
        obj.LengthRev = float(probj.properties["LengthRev"])
        obj.Solid = probj.properties["Solid"]
        obj.Reversed = probj.properties["Reversed"]
        obj.Symmetric = probj.properties["Symmetric"]
        obj.TaperAngle = probj.properties["TaperAngle"]
        obj.TaperAngleRev = probj.properties["TaperAngleRev"]
        doc.recompute()
    except Exception as e:
        FreeCAD.Console.PrintError(f"Object '{obj.__class__}' could not be created: '{str(e)}'.\n")
        return False, str(e)
    try:
        ser = serialize_object(obj)
    except Exception as e:
        FreeCAD.Console.PrintError(f"Object '{obj.__class__}' could not be serialized: '{str(e)}'.\n")
        return False, str(e)
    try:
        text = json.dumps(ser)
        return True, text
    except Exception as e:
        FreeCAD.Console.PrintError(f"Object '{obj.__class__}' could not be serialized: '{str(e)}'.\n")
        return False, str(e)