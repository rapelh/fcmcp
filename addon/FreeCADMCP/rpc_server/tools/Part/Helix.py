import mcp.types as types
import FreeCAD
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue, Object
from rpc_server.tools.App.DocumentObject.New import _create_object_gui

tool_type = types.Tool(
                name="Part-Helix",
                description="Create a named helix object in a named document",
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
                            "Pitch": {
                                "type": "number",
                                "description": "Distance between two consecutive turns of the helix measured along its Z axis. Default 1mm."
                            }, 
                            "Height": {
                                "type": "number",
                                "description": "Height of the helix. Default 2mm."
                            }, 
                            "Radius": {
                                "type": "number",
                                "description": "Start radius of the helix. The helix has a constant radius if Angle is 0°."
                            }, 
                            "SegmentLength": {
                                "type": "integer",
                                "description": "Number of turns per helix subdivision. The default is 1, meaning each full turn of the helix is a separate segment. Use 0 to suppress subdivision."
                            }, 
                            "Angle": {
                                "type": "number",
                                "description": "Angle that defines the outer shape of the helix. Valid range: -90° < value < 90°. Default 0°. If it is 0° the helix is cylindrical, else it is conical."
                            }, 
                        },
                    },
                },
            )

def do_it(args):
    doc_name = args.get("DocName")
    probj = Object(
        name=args.get("ObjName", "Helix"),
        type="Part::Helix",
        analysis=args.get("Analysis", None),
        properties=args.get("Properties", {}),
    )
    rpc_request_queue.put(lambda: _create_object_gui(doc_name, probj))
    res, text = rpc_response_queue.get()
    return [types.TextContent(type="text", text=text)]