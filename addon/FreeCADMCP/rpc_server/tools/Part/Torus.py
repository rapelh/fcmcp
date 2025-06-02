import mcp.types as types
import FreeCAD
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue, Object
from rpc_server.tools.App.DocumentObject.New import _create_object_gui

tool_type = types.Tool(
                name="Part-Torus",
                description="Create a named torus object in a named document",
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
                                "type": "number",
                                "description": "Radius of the circular path of the torus. Default 10mm."
                            }, 
                            "Radius2": {
                                "type": "number",
                                "description": "Radius of the circular profile of the torus. Default 2mm."
                            }, 
                            "Angle1": {
                                "type": "number",
                                "description": "Start angle of the circular profile. Valid range: -180° <= value <= 180°. Default -180°."
                            }, 
                            "Angle2": {
                                "type": "number",
                                "description": "End angle of the circular profile. Valid range: -180° <= value <= 180°. Default -180°."
                            }, 
                            "Angle3": {
                                "type": "number",
                                "description": "Angle of the circular path of the torus. Valid range: 0° < value <= 360°. Default 360°."
                            }, 
                        },
                    },
                },
            )

def do_it(args):
    doc_name = args.get("Doc")
    obj = Object(
        name=args.get("Name", "Torus"),
        type="Part::Torus",
        analysis=args.get("Analysis", None),
        properties=args.get("Properties", {}),
    )
    rpc_request_queue.put(lambda: _create_object_gui(doc_name, obj))
    res, text = rpc_response_queue.get()
    return [types.TextContent(type="text", text=text)]