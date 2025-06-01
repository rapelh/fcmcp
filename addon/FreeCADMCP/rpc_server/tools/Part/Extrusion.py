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
                    "required": ["Doc", "Name"],
                    "properties": {
                        "Doc": {
                            "type": "string",
                            "description": "Name of document in which to create",
                        },
                        "Name": {
                            "type": "string",
                            "description": "Name of object to create",
                        },
                        "Properties": {
                            "Base": {
                                "type": "string",
                                "description": "Name of base object shape"
                            }, 
                            "DirMode": {
                                "type": "string",
                                "description": "Normal, Edge or Custom."
                            }, 
                            "Dir": {
                                "X": {
                                    "type": "float",
                                    "description": "X component of direction"
                                },
                                "Y": {
                                    "type": "float",
                                    "description": "Y component of direction"
                                },
                                "Z": {
                                    "type": "float",
                                    "description": "Z component of direction"
                                }
                            }, 
                            "DirLink": {
                                "type": "string",
                                "description": "Link to object for Normal or Edge DirMode"
                            }, 
                            "LengthFwd": {
                                "type": "float",
                                "description": "Length to extrude forward"
                            }, 
                            "LengthRev": {
                                "type": "float",
                                "description": "Length to extrude reverse"
                            }, 
                            "Solid": {
                                "type": "bool",
                                "description": "Create solid"
                            }, 
                            "Reversed": {
                                "type": "bool",
                                "description": "Direction reversed"
                            }, 
                            "Symmetric": {
                                "type": "bool",
                                "description": "Extrude symmetric"
                            }, 
                            "TaperAngle": {
                                "type": "float",
                                "description": "Taper angle forward"
                            }, 
                            "TaperAngleRev": {
                                "type": "float",
                                "description": "Taper angle reverse"
                            }, 
                        },
                    },
                },
            )

def do_it(args):
    doc_name = args.get("Doc")
    obj = Object(
        name=args.get("Name", "Extrude"),
        type="Part::Extrusion",
        analysis=args.get("Analysis", None),
        properties=args.get("Properties", {}),
    )
    rpc_request_queue.put(lambda: _extrude_shape_gui(doc_name, obj))
    res, text = rpc_response_queue.get()
    return [types.TextContent(type="text", text=text)]

def _extrude_shape_gui(doc_name, obj_in):
    doc = FreeCAD.getDocument(doc_name)
    if not doc:
        FreeCAD.Console.PrintError(f"Document '{doc_name}' not found.\n")
        return False, f"Document '{doc_name}' not found.\n"
    try:
        obj = doc.addObject(obj_in.type, obj_in.name)
        obj.Base = doc.getObject(obj_in.properties["Base"])
        obj.DirMode = obj_in.properties["DirMode"]
        obj.DirLink = doc.getObject(obj_in.properties["DirLink"])
        obj.Dir = FreeCAD.Vector(obj_in.properties["Dir"]["X"], obj_in.properties["Dir"]["Y"], obj_in.properties["Dir"]["Z"])
        obj.LengthFwd = float(obj_in.properties["LengthFwd"])
        obj.LengthRev = float(obj_in.properties["LengthRev"])
        obj.Solid = obj_in.properties["Solid"]
        obj.Reversed = obj_in.properties["Reversed"]
        obj.Symmetric = obj_in.properties["Symmetric"]
        obj.TaperAngle = obj_in.properties["TaperAngle"]
        obj.TaperAngleRev = obj_in.properties["TaperAngleRev"]
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