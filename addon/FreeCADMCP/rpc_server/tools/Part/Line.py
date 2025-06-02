import mcp.types as types
import FreeCAD
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue, Object
from rpc_server.tools.App.DocumentObject.New import _create_object_gui

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
                                "type": "number",
                                "description": "X coordinate of the start point. Default 0mm."
                            }, 
                            "Y1": {
                                "type": "number",
                                "description": "Y coordinate of the start point. Default 0mm."
                            }, 
                            "Z1": {
                                "type": "number",
                                "description": "Z coordinate of the start point. Default 0mm."
                            }, 
                            "X2": {
                                "type": "number",
                                "description": "X coordinate of the start point. Default 10mm."
                            }, 
                            "Y2": {
                                "type": "number",
                                "description": "Y coordinate of the start point. Default 10mm."
                            }, 
                            "Z2": {
                                "type": "number",
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
    rpc_request_queue.put(lambda: _create_object_gui(doc_name, obj))
    res, text = rpc_response_queue.get()
    return [types.TextContent(type="text", text=text)]