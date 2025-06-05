import mcp.types as types
import FreeCAD
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue, Object
from rpc_server.tools.App.DocumentObject.New import _create_object_gui

tool_type = types.Tool(
                name="Part-Sphere",
                description="Create a named sphere object in a named document",
                inputSchema={
                    "type": "object",
                    "required": ["DocName", "ObjName"],
                    "properties": {
                        "DocName": {
                            "type": "string",
                            "description": "Name of document in which to create",
                        },
                        "ObjName": {
                            "type": "string",
                            "description": "Name of object to create",
                        },
                        "Properties": {
                            "Radius": {
                                "type": "number",
                                "description": "Radius of the sphere to create",
                            },
                            "Angle1": {
                                "type": "number",
                                "description": "The start angle of the circular arc profile of the sphere. Valid range: -90° <= value <= 90°. Default -90°.",
                            },
                            "Angle2": {
                                "type": "number",
                                "description": "The end angle of the circular arc profile of the sphere. Valid range: -90° <= value <= 90°. Default 90°.",
                            },
                            "Angle3": {
                                "type": "number",
                                "description": "The total angle of revolution of the sphere. Valid range: 0° < value <= 360°. Default 360°.",
                            }
                        }
                    },
                },
            )

def do_it(args):
    doc_name = args.get("DocName")
    obj = Object(
        name=args.get("ObjectName", "Sphere"),
        type="Part::Sphere",
        analysis=args.get("Analysis", None),
        properties=args.get("Properties", {}),
    )
    rpc_request_queue.put(lambda: _create_object_gui(doc_name, obj))
    res, text = rpc_response_queue.get()
    return [types.TextContent(type="text", text=text)]