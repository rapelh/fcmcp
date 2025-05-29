import mcp.types as types
import FreeCAD
from sse_server.sse_server import sse_request_queue, sse_response_queue, set_object_property, Object
from addon.FreeCADMCP.sse_server.tools.App.DocumentObject.New import _create_object_gui

tool_type = types.Tool(
                name="Part-Box",
                description="Create a named box object in a named document",
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
                    },
                },
            )

def do_it(args):
    doc_name = args.get("Doc")
    obj = Object(
        name=args.get("Name", "New_Object"),
        type="Part::Box",
        analysis=args.get("Analysis", None),
        properties=args.get("Properties", {}),
    )
    sse_request_queue.put(lambda: _create_object_gui(doc_name, obj))
    res = sse_response_queue.get()
    if res is True:
        return [types.TextContent(type="text", text=obj.name)]
    else:
        return [types.TextContent(type="text", text=res)]
