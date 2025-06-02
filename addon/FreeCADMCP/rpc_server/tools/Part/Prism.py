import mcp.types as types
import FreeCAD
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue, Object
from rpc_server.tools.App.DocumentObject.New import _create_object_gui

tool_type = types.Tool(
                name="Part-Prism",
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
                            "Polygon": {
                                "type": "integer",
                                "description": "Number of sides of the polygon. Default 6."
                            }, 
                            "Circumradius": {
                                "type": "number",
                                "description": "Radius of the circle that circumscribes the polygon, the distance from the center of the polygon to one of its vertices. Default 2mm."
                            }, 
                            "Height": {
                                "type": "number",
                                "description": "Height of the prism. Default 10mm."
                            }, 
                            "FirstAngle": {
                                "type": "number",
                                "description": "Angle between the extrusion direction of the prism and the positive Z axis, measured around the Y axis. Positive towards the positive X axis. Valid range: 0° <= value < 90°. Default 0°."
                            }, 
                            "SecondAngle": {
                                "type": "number",
                                "description": "Angle between the extrusion direction of the prism and its positive Z axis, measured around its X axis. Positive towards its positive Y axis. Valid range: 0° <= value < 90°. Default 0°."
                            }, 
                        },
                    },
                },
            )

def do_it(args):
    doc_name = args.get("Doc")
    obj = Object(
        name=args.get("Name", "Prism"),
        type="Part::Prism",
        analysis=args.get("Analysis", None),
        properties=args.get("Properties", {}),
    )
    rpc_request_queue.put(lambda: _create_object_gui(doc_name, obj))
    res, text = rpc_response_queue.get()
    return [types.TextContent(type="text", text=text)]