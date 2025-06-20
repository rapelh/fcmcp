import mcp.types as types
import FreeCAD
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue, Object
from rpc_server.tools.App.DocumentObject.New import _create_object_gui

tool_type = types.Tool(
                name="Part-Cylinder",
                description="Create a named cylinder object in a named document",
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
                                "description": "Radius of the cylinder to create",
                            },
                            "Height": {
                                "type": "number",
                                "description": "Height of the cylinder to create",
                            },
                            "Angle": {
                                "type": "number",
                                "description": "Circular arc of the cylinder to create. Valid range: 0° < value <= 360°. Default 360°.",
                            },
                            "FirstAngle": {
                                "type": "number",
                                "description": "The angle between the extrusion direction of the cylinder and the positive Z axis, measured around the Y axis. Valid range: 0° <= value < 90°. Default 0°.",
                            },
                            "SecondAngle": {
                                "type": "number",
                                "description": "The angle between the extrusion direction of the cylinder and the positive Z axis, measured around the X axis. Valid range: 0° <= value < 90°. Default 0°.",
                            }
                        },
                    },
                },
            )

def do_it(args):
    doc_name = args.get("DocName")
    probj = Object(
        name=args.get("ObjName", "Cylinder"),
        type="Part::Cylinder",
        analysis=args.get("Analysis", None),
        properties=args.get("Properties", {}),
    )
    rpc_request_queue.put(lambda: _create_object_gui(doc_name, probj))
    res, text = rpc_response_queue.get()
    return [types.TextContent(type="text", text=text)]