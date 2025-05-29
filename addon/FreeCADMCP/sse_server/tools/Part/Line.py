import mcp.types as types
import FreeCAD
from sse_server.sse_server import sse_request_queue, sse_response_queue, Object
from sse_server.tools.App.DocumentObject.New import _create_object_gui

tool_type = types.Tool(
                name="Part-Line",
                description="Create a named line object in a named document",
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
                            "X1": {
                                "type": "float",
                                "description": "X coordinate of the start point. Default 0mm."
                            }, 
                            "Y1": {
                                "type": "float",
                                "description": "Y coordinate of the start point. Default 0mm."
                            }, 
                            "Z1": {
                                "type": "float",
                                "description": "Z coordinate of the start point. Default 0mm."
                            }, 
                            "X2": {
                                "type": "float",
                                "description": "X coordinate of the start point. Default 10mm."
                            }, 
                            "Y2": {
                                "type": "float",
                                "description": "Y coordinate of the start point. Default 10mm."
                            }, 
                            "Z2": {
                                "type": "float",
                                "description": "Z coordinate of the start point. Default 10mm."
                            }, 
                        },
                    },
                },
            )

def do_it(args):
    doc_name = args.get("Doc")
    obj = Object(
        name=args.get("Name", "Line"),
        type="Part::Line",
        analysis=args.get("Analysis", None),
        properties=args.get("Properties", {}),
    )
    sse_request_queue.put(lambda: _create_object_gui(doc_name, obj))
    res = sse_response_queue.get()
    if res is True:
        return [types.TextContent(type="text", text=obj.name)]
    else:
        return [types.TextContent(type="text", text=res)]
