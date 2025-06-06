import mcp.types as types
import FreeCAD
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue, Object
from rpc_server.tools.App.DocumentObject.New import _create_object_gui

tool_type = types.Tool(
                name="Part-Wedge",
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
                            "Xmin": {
                                "type": "number",
                                "description": "Lowest X coordinate of the front face of the wedge. Default 0mm."
                            }, 
                            "Ymin": {
                                "type": "number",
                                "description": "Y coordinate of the front face of the wedge. Default 0mm."
                            }, 
                            "Zmin": {
                                "type": "number",
                                "description": "Lowest Z coordinate of the front face of the wedge. Default 0mm."
                            }, 
                            "X2min": {
                                "type": "number",
                                "description": "Lowest X coordinate of the rear face of the wedge. Default 2mm."
                            }, 
                            "Z2min": {
                                "type": "number",
                                "description": "Lowest Z coordinate of the rear face of the wedge. Default 2mm."
                            }, 
                            "Xmax": {
                                "type": "number",
                                "description": "Highest X coordinate of the front face of the wedge. Default 10mm."
                            }, 
                            "Ymax": {
                                "type": "number",
                                "description": "Y coordinate of the rear face of the wedge. Default 10mm."
                            }, 
                            "Zmax": {
                                "type": "number",
                                "description": "Highest Z coordinate of the front face of the wedge. Default 10mm."
                            }, 
                            "X2max": {
                                "type": "number",
                                "description": "Highest X coordinate of the rear face of the wedge. Default 8mm."
                            }, 
                            "Z2max": {
                                "type": "number",
                                "description": "Highest Z coordinate of the rear face of the wedge. Default 8mm."
                            }, 
                        },
                    },
                },
            )

def do_it(args):
    doc_name = args.get("DocName")
    probj = Object(
        name=args.get("ObjName", "Wedge"),
        type="Part::Wedge",
        analysis=args.get("Analysis", None),
        properties=args.get("Properties", {}),
    )
    rpc_request_queue.put(lambda: _create_object_gui(doc_name, probj))
    res, text = rpc_response_queue.get()
    return [types.TextContent(type="text", text=text)]