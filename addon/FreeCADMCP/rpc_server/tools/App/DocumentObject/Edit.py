import mcp.types as types
import FreeCAD
import json
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue, set_object_property, Object
from rpc_server.serialize import serialize_object

tool_type = types.Tool(
                name="App-DocumentObject-Edit",
                description="Modify properties of a named object in a named document",
                inputSchema={
                    "type": "object",
                    "required": ["DocName", "ObjName"],
                    "properties": {
                        "DocName": {
                            "type": "string",
                            "description": "Name of document the object belongs to",
                        },
                        "ObjName": {
                            "type": "string",
                            "description": "Name of object to modify",
                        },
                        "Properties": {
                            "Length": {
                                "type": "number",
                                "description": "Length of object to set",
                            },
                            "Width": {
                                "type": "number",
                                "description": "Width of object to set",
                            },
                            "Height": {
                                "type": "number",
                                "description": "Height of object to set",
                            },
                            "Radius": {
                                "type": "number",
                                "description": "Radius of object to set",
                            }
                        }
                    },
                },
            )

def do_it(args):
    doc_name = args.get('DocName')
    obj_name = args.get('ObjName')
    probj = Object(
        name=obj_name,
        properties=args.get("Properties", {}),
    )
    rpc_request_queue.put(lambda: _edit_object_gui(doc_name, probj))
    res, text = rpc_response_queue.get()
    if res is True:
        return [types.TextContent(type="text", text=text)]
    else:
        return [types.TextContent(type="text", text=text)]

def _edit_object_gui(doc_name: str, probj: Object):
    doc = FreeCAD.getDocument(doc_name)
    if not doc:
        FreeCAD.Console.PrintError(f"Document '{doc_name}' not found.\n")
        return False, f"Document '{doc_name}' not found.\n"

    obj = doc.getObject(probj.name)
    if not obj:
        FreeCAD.Console.PrintError(f"Object '{pr.name}' not found in document '{doc_name}'.\n")
        return False, f"Object '{probj.name}' not found in document '{doc_name}'.\n"

    try:
        # For Fem::ConstraintFixed
        if hasattr(obj, "References") and "References" in probj.properties:
            refs = []
            for ref_name, face in probj.properties["References"]:
                ref_obj = doc.getObject(ref_name)
                if ref_obj:
                    refs.append((ref_obj, face))
                else:
                    raise ValueError(f"Referenced object '{ref_name}' not found.")
            obj.References = refs
            FreeCAD.Console.PrintMessage(
                f"References updated for '{probj.name}' in '{doc_name}'.\n"
            )
            # delete References from properties
            del probj.properties["References"]
        set_object_property(doc, obj, probj.properties)
        doc.recompute()
        FreeCAD.Console.PrintMessage(f"Object '{probj.name}' updated via RPC.\n")
        return True, json.dumps(serialize_object(obj))
    except Exception as e:
        return str(e)
