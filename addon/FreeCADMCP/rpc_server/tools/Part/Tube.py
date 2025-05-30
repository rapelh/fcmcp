import mcp.types as types
import FreeCAD
from addon.FreeCADMCP.rcp_server.rpc_server import rcp_request_queue, rcp_response_queue, Object
from rcp_server.tools.App.DocumentObject.New import _create_object_gui

tool_type = types.Tool(
                name="Part-Tube",
                description="Create a named tube object in a named document",
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
                            "Height": {
                                "type": "float",
                                "description": "Height of the tube. The default is 10mm."
                            }, 
                            "InnerRadius": {
                                "type": "float",
                                "description": "Inner radius of the tube. Must be smaller than OuterRadius. Can be 0. Default 2mm."
                            }, 
                            "OuterRadius": {
                                "type": "float",
                                "description": "Outer radius of the tube. Must be larger than InnerRadius. Default 5mm."
                            }, 
                        },
                    },
                },
            )

def do_it(args):
    doc_name = args.get("Doc")
    obj = Object(
        name=args.get("Name", "Tube"),
        type="Part::Tube",
        analysis=args.get("Analysis", None),
        properties=args.get("Properties", {}),
    )
    rcp_request_queue.put(lambda: _create_object_gui(doc_name, obj))
    res = rcp_response_queue.get()
    if res is True:
        return [types.TextContent(type="text", text=obj.name)]
    else:
        return [types.TextContent(type="text", text=res)]
