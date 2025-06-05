import mcp.types as types
import FreeCAD
import Draft
import json
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue, Object
from rpc_server.serialize import serialize_object

tool_type = types.Tool(
                name="Draft-Line-FromVectors",
                description="Create a labeled line object from vectors in a named document",
                inputSchema={
                    "type": "object",
                    "required": ["DocName"],
                    "properties": {
                        "DocName": {
                            "type": "string",
                            "description": "Name of document in which to create",
                        },
                        "ObjLabel": {
                            "type": "string",
                            "description": "Label for object to create",
                        },
                        "Properties": {
                            "RefObjectName": {
                                "type": "string",
                                "description": "Name of object the shape belongs to."
                            }, 
                        },
                    },
                },
            )

def do_it(args):
    doc_name = args.get("DocName")
    label = args.get("ObjLabel")
    obj = Object(
        name=label,
        properties=args.get("Properties", {}),
    )
    rpc_request_queue.put(lambda: _line_from_shape_gui(doc_name, label, obj))
    res, text = rpc_response_queue.get()
    return [types.TextContent(type="text", text=text)]

def _line_from_shape_gui(doc_name, label, obj):
    doc = FreeCAD.getDocument(doc_name)
    ref_obj = doc.getObject(obj.properties["RefObjectName"])
    line = Draft.make_line(ref_obj.Shape)
    line.Label = label
    doc.recompute()
    try:
        ser = serialize_object(line)
    except Exception as e:
        return False, str(e)
    try:
        text = json.dumps(ser)
        return True, text
    except Exception as e:
        return False, str(e)