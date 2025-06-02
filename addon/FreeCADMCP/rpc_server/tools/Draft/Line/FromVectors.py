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
                            "X1": {
                                "type": "float",
                                "description": "X coordinate of the first vector. Default 0mm."
                            }, 
                            "Y1": {
                                "type": "float",
                                "description": "Y coordinate of the first vector. Default 0mm."
                            }, 
                            "Z1": {
                                "type": "float",
                                "description": "Z coordinate of the first vector. Default 0mm."
                            }, 
                            "X2": {
                                "type": "float",
                                "description": "X coordinate of the second vector. Default 10mm."
                            }, 
                            "Y2": {
                                "type": "float",
                                "description": "Y coordinate of the second vector. Default 10mm."
                            }, 
                            "Z2": {
                                "type": "float",
                                "description": "Z coordinate of the second vector. Default 10mm."
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
    rpc_request_queue.put(lambda: _line_from_vectors_gui(doc_name, label, obj))
    res, text = rpc_response_queue.get()
    return [types.TextContent(type="text", text=text)]

def _line_from_vectors_gui(doc_name, label, obj):
    doc = FreeCAD.getDocument(doc_name)
    p1 = FreeCAD.Vector(obj.properties["X1"], obj.properties["Y1"], obj.properties["Z1"])
    p2 = FreeCAD.Vector(obj.properties["X2"], obj.properties["Y2"], obj.properties["Z2"])
    line = Draft.make_line(p1, p2)
    line.Label = label
    doc.recompute()
    return True, line.Label