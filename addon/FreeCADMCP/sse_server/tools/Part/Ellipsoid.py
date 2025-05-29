import mcp.types as types
import FreeCAD
from sse_server.sse_server import sse_request_queue, sse_response_queue, Object
from sse_server.tools.App.DocumentObject.New import _create_object_gui

tool_type = types.Tool(
                name="Part-Ellipsoid",
                description="Create a named ellipsoid object in a named document",
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
                                "description": "Radius of the ellipsoid in the Z direction. Default 2mm."
                            }, 
                            "Radius2": {
                                "type": "float",
                                "description": "Radius of the ellipsoid in the X direction. Default 4mm."
                            }, 
                            "Radius3": {
                                "type": "float",
                                "description": "Radius of the ellipsoid in the Y direction. Default 4mm."
                            }, 
                            "Angle1": {
                                "type": "float",
                                "description": "Start angle of the elliptical sides of the ellipsoid. Valid range: -90° <= value < 90°. Must be smaller than Angle2. Default -90°."
                            }, 
                            "Angle2": {
                                "type": "float",
                                "description": "End angle of the elliptical sides of the ellipsoid. Valid range: -90° <= value < 90°. Must be larger than Angle1. Default 90°."
                            }, 
                            "Angle3": {
                                "type": "float",
                                "description": "Total angle of the ellipsoid in its XY plane. Valid range: 0° < value <= 360°. Default 360°."
                            }, 
                        },
                    },
                },
            )

def do_it(args):
    doc_name = args.get("Doc")
    obj = Object(
        name=args.get("Name", "Ellipsoid"),
        type="Part::Ellipsoid",
        analysis=args.get("Analysis", None),
        properties=args.get("Properties", {}),
    )
    sse_request_queue.put(lambda: _create_object_gui(doc_name, obj))
    res = sse_response_queue.get()
    if res is True:
        return [types.TextContent(type="text", text=obj.name)]
    else:
        return [types.TextContent(type="text", text=res)]
