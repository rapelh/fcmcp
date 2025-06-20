import mcp.types as types
import FreeCAD
import Draft
import json
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue, Object
from rpc_server.serialize import serialize_object

tool_type = types.Tool(
                name="Draft-Line-FromLineSegment",
                description="Create a labeled line object from a sketcher geometry line segment in a named document",
                inputSchema={
                    "type": "object",
                    "required": ["DocName"],
                    "properties": {
                        "DocName": {
                            "type": "string",
                            "description": "Name of document in which to create",
                        },
                        "ObjLabel": {
                            "type": "string",
                            "description": "Label for object to create",
                        },
                        "Properties": {
                            "SketchName": {
                                "type": "string",
                                "description": "Sketcher object name"
                            }, 
                            "GeometryIndex": {
                                "type": "integer",
                                "description": "Index of LineSegment in Sketcher object geometry"
                            }, 
                        },
                    },
                },
            )

def do_it(args):
    doc_name = args.get("DocName")
    label = args.get("ObjLabel")
    probj = Object(
        name=label,
        properties=args.get("Properties", {}),
    )
    rpc_request_queue.put(lambda: _line_from_sketch_line_segment_gui(doc_name, label, probj))
    res, text = rpc_response_queue.get()
    return [types.TextContent(type="text", text=text)]

def _line_from_sketch_line_segment_gui(doc_name, label, probj):
    doc = FreeCAD.getDocument(doc_name)
    sketch = doc.getObject(probj.properties["SketchName"])
    ls = sketch.Geometry[probj.properties["GeometryIndex"]]
    line = Draft.make_line(ls)
    line.Label = label
    doc.recompute()
    try:
        ser = serialize_object(line)
    except Exception as e:
        return False, str(e)
    try:
        text = json.dumps(ser)
        return True, text
    except Exception as e:
        return False, str(e)
