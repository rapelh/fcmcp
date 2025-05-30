import mcp.types as types
import FreeCAD
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue, Object
from rpc_server.tools.App.DocumentObject.New import _create_object_gui

tool_type = types.Tool(
                name="Part-Spiral",
                description="Create a named spiral object in a named document",
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
                            "Growth": {
                                "type": "float",
                                "description": "Distance between two consecutive turns of the spiral. Default 1mm."
                            }, 
                            "Rotations": {
                                "type": "int",
                                "description": "Number of rotations, or turns, of the spiral. The default is 2."
                            }, 
                            "Radius": {
                                "type": "float",
                                "description": "Start radius of the spiral, the distance between its center and its start point. Can be 0mm. Default 1mm."
                            }, 
                            "SegmentLength": {
                                "type": "int",
                                "description": "Number of turns per spiral subdivision. The default is 1, meaning each full turn of the spiral is a separate segment. Use 0 to suppress subdivision."
                            }, 
                        },
                    },
                },
            )

def do_it(args):
    doc_name = args.get("Doc")
    obj = Object(
        name=args.get("Name", "Spiral"),
        type="Part::Spiral",
        analysis=args.get("Analysis", None),
        properties=args.get("Properties", {}),
    )
    rpc_request_queue.put(lambda: _create_object_gui(doc_name, obj))
    res = rpc_response_queue.get()
    if res is True:
        return [types.TextContent(type="text", text=obj.name)]
    else:
        return [types.TextContent(type="text", text=res)]
