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
                            "X1": {
                                "type": "float",
                                "description": "X coordinate of the start point. Default 0mm."
                            }, 
                            "Y1": {
                                "type": "float",
                                "description": "Y coordinate of the start point. Default 0mm."
                            }, 
                            "Z1": {
                                "type": "float",
                                "description": "Z coordinate of the start point. Default 0mm."
                            }, 
                            "X2": {
                                "type": "float",
                                "description": "X coordinate of the start point. Default 10mm."
                            }, 
                            "Y2": {
                                "type": "float",
                                "description": "Y coordinate of the start point. Default 10mm."
                            }, 
                            "Z2": {
                                "type": "float",
                                "description": "Z coordinate of the start point. Default 10mm."
                            }, 
                        },
                    },
                },
            )

def do_it(args):
    doc_name = args.get("Doc")
    obj = Object(
        name=args.get("Name", "Line"),
        type="Part::LineSegment",
        analysis=args.get("Analysis", None),
        properties=args.get("Properties", {}),
    )
    rpc_request_queue.put(lambda: _create_line_segment_gui(doc_name, obj))
    res, text = rpc_response_queue.get()
    return [types.TextContent(type="text", text=text)]

def _create_line_segment_gui(doc_name, obj):
    doc = FreeCAD.getDocument(doc_name)
    line = Part.LineSegment()
    line.StartPoint = (obj.properties["X1"], obj.properties["Y1"], obj.properties["Z1"])
    line.EndPoint = (obj.properties["X2"], obj.properties["Y2"], obj.properties["Z2"])
    obj_ins = doc.addObject("Part::Feature", obj.name)
    obj_ins.Shape= line.toShape()
    doc.recompute()
    return True, json.dumps(serialize_object(obj_ins))