import mcp.types as types
import FreeCAD
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue, Object
from rpc_server.tools.App.DocumentObject.New import _create_object_gui

tool_type = types.Tool(
                name="Part-RegularPolygon",
                description="Create a named tube object in a named document",
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
                            "Polygon": {
                                "type": "integer",
                                "description": "Number of sides of the polygon. Default 6."
                            }, 
                            "Circumradius": {
                                "type": "number",
                                "description": "Radius of the circle that circumscribes the polygon, the distance from the center of the polygon to one of its vertices. Default 2mm."
                            }, 
                        },
                    },
                },
            )

def do_it(args):
    doc_name = args.get("DocName")
    probj = Object(
        name=args.get("ObjName", "RegularPolygon"),
        type="Part::RegularPolygon",
        analysis=args.get("Analysis", None),
        properties=args.get("Properties", {}),
    )
    rpc_request_queue.put(lambda: _create_object_gui(doc_name, probj))
    res, text = rpc_response_queue.get()
    return [types.TextContent(type="text", text=text)]