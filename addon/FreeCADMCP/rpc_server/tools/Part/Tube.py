import mcp.types as types
import FreeCAD
import json
from BasicShapes import Shapes
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue, set_object_property, Object
from rpc_server.serialize import serialize_object

tool_type = types.Tool(
                name="Part-Tube",
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
                            "Height": {
                                "type": "number",
                                "description": "Height of the tube. The default is 10mm."
                            }, 
                            "InnerRadius": {
                                "type": "number",
                                "description": "Inner radius of the tube. Must be smaller than OuterRadius. Can be 0. Default 2mm."
                            }, 
                            "OuterRadius": {
                                "type": "number",
                                "description": "Outer radius of the tube. Must be larger than InnerRadius. Default 5mm."
                            }, 
                        },
                    },
                },
            )

def do_it(args):
    doc_name = args.get("DocName")
    probj = Object(
        name=args.get("ObjName", "Tube"),
        type="Part::Tube",
        analysis=args.get("Analysis", None),
        properties=args.get("Properties", {}),
    )
    rpc_request_queue.put(lambda: _create_tube_gui(doc_name, probj))
    res, text = rpc_response_queue.get()
    return [types.TextContent(type="text", text=text)]

def _create_tube_gui(doc_name, probj):
    doc = FreeCAD.getDocument(doc_name)
    tube = Shapes.addTube(doc, probj.name)
    set_object_property(doc, tube, probj.properties)
    doc.recompute()
    return True, json.dumps(serialize_object(tube))