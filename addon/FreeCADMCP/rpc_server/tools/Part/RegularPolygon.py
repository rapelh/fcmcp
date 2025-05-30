import mcp.types as types
import FreeCAD
from addon.FreeCADMCP.rcp_server.rpc_server import rcp_request_queue, rcp_response_queue, Object
from rcp_server.tools.App.DocumentObject.New import _create_object_gui

tool_type = types.Tool(
                name="Part-RegularPolygon",
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
                                "type": "int",
                                "description": "Number of sides of the polygon. Default 6."
                            }, 
                            "Circumradius": {
                                "type": "float",
                                "description": "Radius of the circle that circumscribes the polygon, the distance from the center of the polygon to one of its vertices. Default 2mm."
                            }, 
                        },
                    },
                },
            )

def do_it(args):
    doc_name = args.get("Doc")
    obj = Object(
        name=args.get("Name", "RegularPolygon"),
        type="Part::RegularPolygon",
        analysis=args.get("Analysis", None),
        properties=args.get("Properties", {}),
    )
    rcp_request_queue.put(lambda: _create_object_gui(doc_name, obj))
    res = rcp_response_queue.get()
    if res is True:
        return [types.TextContent(type="text", text=obj.name)]
    else:
        return [types.TextContent(type="text", text=res)]
