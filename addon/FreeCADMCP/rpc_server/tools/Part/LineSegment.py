import mcp.types as types
import FreeCAD
import Part
import json
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue, Object
from rpc_server.serialize import serialize_object

tool_type = types.Tool(
                name="Part-LineSegment",
                description="Create a named line segment object in a named document",
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
                            "X1": {
                                "type": "number",
                                "description": "X coordinate of the start point. Default 0mm."
                            }, 
                            "Y1": {
                                "type": "number",
                                "description": "Y coordinate of the start point. Default 0mm."
                            }, 
                            "Z1": {
                                "type": "number",
                                "description": "Z coordinate of the start point. Default 0mm."
                            }, 
                            "X2": {
                                "type": "number",
                                "description": "X coordinate of the start point. Default 10mm."
                            }, 
                            "Y2": {
                                "type": "number",
                                "description": "Y coordinate of the start point. Default 10mm."
                            }, 
                            "Z2": {
                                "type": "number",
                                "description": "Z coordinate of the start point. Default 10mm."
                            }, 
                        },
                    },
                },
            )

def do_it(args):
    doc_name = args.get("DocName")
    probj = Object(
        name=args.get("ObjName", "Line"),
        type="Part::LineSegment",
        analysis=args.get("Analysis", None),
        properties=args.get("Properties", {}),
    )
    rpc_request_queue.put(lambda: _create_line_segment_gui(doc_name, probj))
    res, text = rpc_response_queue.get()
    return [types.TextContent(type="text", text=text)]

def _create_line_segment_gui(doc_name, probj):
    doc = FreeCAD.getDocument(doc_name)
    line = Part.LineSegment()
    line.StartPoint = (probj.properties["X1"], probj.properties["Y1"], probj.properties["Z1"])
    line.EndPoint = (probj.properties["X2"], probj.properties["Y2"], probj.properties["Z2"])
    obj = doc.addObject("Part::Feature", probj.name)
    obj.Shape= line.toShape()
    doc.recompute()
    return True, json.dumps(serialize_object(obj))