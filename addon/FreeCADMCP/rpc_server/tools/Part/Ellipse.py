import mcp.types as types
import FreeCAD
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue, Object
from rpc_server.tools.App.DocumentObject.New import _create_object_gui

tool_type = types.Tool(
                name="Part-Ellipse",
                description="Create a named ellipse object in a named document",
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
                            "MajorRadius": {
                                "type": "number",
                                "description": "Major radius of the ellipse or elliptical arc. Default 4mm."
                            }, 
                            "MinorRadius": {
                                "type": "number",
                                "description": "Minor radius of the ellipse or elliptical arc. Default 2mm."
                            }, 
                            "Angle1": {
                                "type": "number",
                                "description": "Start angle of the elliptical arc. Valid range: 0° < value <= 360°. Default 0°."
                            }, 
                            "Angle2": {
                                "type": "number",
                                "description": "End angle of the elliptical arc. Valid range: 0° < value <= 360°. Default 360°."
                            }, 
                        },
                    },
                },
            )

def do_it(args):
    doc_name = args.get("DocName")
    obj = Object(
        name=args.get("ObjName", "Ellipse"),
        type="Part::Ellipse",
        analysis=args.get("Analysis", None),
        properties=args.get("Properties", {}),
    )
    rpc_request_queue.put(lambda: _create_object_gui(doc_name, obj))
    res, text = rpc_response_queue.get()
    return [types.TextContent(type="text", text=text)]