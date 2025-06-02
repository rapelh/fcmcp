import mcp.types as types
import FreeCAD
import Draft
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue, Object

tool_type = types.Tool(
                name="Draft-Line-FromLineSegment",
                description="Create a labeled line object from a sketcher geometry line segment in a named document",
                inputSchema={
                    "type": "object",
                    "required": ["Doc"],
                    "properties": {
                        "Doc": {
                            "type": "string",
                            "description": "Name of document in which to create",
                        },
                        "Label": {
                            "type": "string",
                            "description": "Label for object to create",
                        },
                        "Properties": {
                            "SketchName": {
                                "type": "string",
                                "description": "Sketcher object name"
                            }, 
                            "GeometryIndex": {
                                "type": "int",
                                "description": "Index of LineSegment in Sketcher object geometry"
                            }, 
                        },
                    },
                },
            )

def do_it(args):
    doc_name = args.get("Doc")
    label = args.get("Label")
    obj = Object(
        name=label,
        properties=args.get("Properties", {}),
    )
    rpc_request_queue.put(lambda: _line_from_sketch_line_segment_gui(doc_name, label, obj))
    res, text = rpc_response_queue.get()
    return [types.TextContent(type="text", text=text)]

def _line_from_sketch_line_segment_gui(doc_name, label, obj):
    doc = FreeCAD.getDocument(doc_name)
    sketch = doc.getObject(obj.properties["SketchName"])
    ls = sketch.Geometry[obj.properties["GeometryIndex"]]
    line = Draft.make_line(ls)
    line.Label = label
    doc.recompute()
    return True, line.Label