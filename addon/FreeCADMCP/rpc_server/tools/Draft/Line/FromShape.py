import mcp.types as types
import FreeCAD
import Draft
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue, Object

tool_type = types.Tool(
                name="Draft-Line-FromVectors",
                description="Create a labeled line object from vectors in a named document",
                inputSchema={
                    "type": "object",
                    "required": ["Doc"],
                    "properties": {
                        "Doc": {
                            "type": "string",
                            "description": "Name of document in which to create",
                        },
                        "Label": {
                            "type": "string",
                            "description": "Label for object to create",
                        },
                        "Properties": {
                            "ObjectName": {
                                "type": "string",
                                "description": "Name of object the shape belongs to."
                            }, 
                        },
                    },
                },
            )

def do_it(args):
    doc_name = args.get("Doc")
    label = args.get("Label")
    obj = Object(
        name=label,
        properties=args.get("Properties", {}),
    )
    rpc_request_queue.put(lambda: _line_from_shape_gui(doc_name, label, obj))
    res, text = rpc_response_queue.get()
    return [types.TextContent(type="text", text=text)]

def _line_from_shape_gui(doc_name, label, obj):
    doc = FreeCAD.getDocument(doc_name)
    ref_obj = doc.getObject(obj.properties["ObjectName"])
    line = Draft.make_line(ref_obj.Shape)
    line.Label = label
    doc.recompute()
    return True, line.Label