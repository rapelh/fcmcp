import mcp.types as types
import FreeCAD
from addon.FreeCADMCP.rpc_server.rpc_server import rpc_request_queue, rpc_response_queue, Object
from rpc_server.tools.App.DocumentObject.New import _create_object_gui

tool_type = types.Tool(
                name="Part-Circle",
                description="Create a named circle object in a named document",
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
                            "Radius": {
                                "type": "float",
                                "description": "Radius of the circle or circular arc. Default 2mm."
                            }, 
                            "Angle1": {
                                "type": "float",
                                "description": "Start angle of the circular arc. Valid range: 0° < value <= 360°. Default 0°."
                            }, 
                            "Angle2": {
                                "type": "float",
                                "description": "End angle of the circular arc. Valid range: 0° < value <= 360°. Default 360°."
                            }, 
                        },
                    },
                },
            )

def do_it(args):
    doc_name = args.get("Doc")
    obj = Object(
        name=args.get("Name", "Circle"),
        type="Part::Circle",
        analysis=args.get("Analysis", None),
        properties=args.get("Properties", {}),
    )
    rpc_request_queue.put(lambda: _create_object_gui(doc_name, obj))
    res = rpc_response_queue.get()
    if res is True:
        return [types.TextContent(type="text", text=obj.name)]
    else:
        return [types.TextContent(type="text", text=res)]
