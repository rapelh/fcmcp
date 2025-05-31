import mcp.types as types
import FreeCAD
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue, Object
from rpc_server.tools.App.DocumentObject.New import _create_object_gui

tool_type = types.Tool(
                name="Part-Cone",
                description="Create a named cone object in a named document",
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
                            "Radius1": {
                                "type": "float",
                                "description": "Radius of the bottom face of the cone. Can be 0mm if Radius2 > 0mm. Default 2mm."
                            },
                            "Radius2": {
                                "type": "float",
                                "description": "Radius of the top face of the cone. Can be 0mm if Radius1 > 0mm. Default 4mm."
                            },
                            "Height": {
                                "type": "float",
                                "description": "Height of the cone. Default 10mm."
                            },
                            "Angle": {
                                "type": "flot",
                                "description": "Angle of the circular arc that defines the top and bottom face of the cone. Valid range: 0° < value <= 360°. Default 360°."
                            },
                        }
                    },
                },
            )

def do_it(args):
    doc_name = args.get("Doc")
    obj = Object(
        name=args.get("Name", "Cone"),
        type="Part::Cone",
        analysis=args.get("Analysis", None),
        properties=args.get("Properties", {}),
    )
    rpc_request_queue.put(lambda: _create_object_gui(doc_name, obj))
    res, text = rpc_response_queue.get()
    return [types.TextContent(type="text", text=text)]