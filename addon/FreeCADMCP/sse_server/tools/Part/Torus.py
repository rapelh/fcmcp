import mcp.types as types
import FreeCAD
from sse_server.sse_server import sse_request_queue, sse_response_queue, Object
from sse_server.tools.App.DocumentObject.New import _create_object_gui

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
                                "type": "float",
                                "description": "Radius of the circular path of the torus. Default 10mm."
                            }, 
                            "Radius2": {
                                "type": "float",
                                "description": "Radius of the circular profile of the torus. Default 2mm."
                            }, 
                            "Angle1": {
                                "type": "float",
                                "description": "Start angle of the circular profile. Valid range: -180° <= value <= 180°. Default -180°."
                            }, 
                            "Angle2": {
                                "type": "float",
                                "description": "End angle of the circular profile. Valid range: -180° <= value <= 180°. Default -180°."
                            }, 
                            "Angle3": {
                                "type": "float",
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
    sse_request_queue.put(lambda: _create_object_gui(doc_name, obj))
    res = sse_response_queue.get()
    if res is True:
        return [types.TextContent(type="text", text=obj.name)]
    else:
        return [types.TextContent(type="text", text=res)]
