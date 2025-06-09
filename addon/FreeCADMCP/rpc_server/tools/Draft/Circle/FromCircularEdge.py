import mcp.types as types
import FreeCAD
import Draft
import json
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue, Object
from rpc_server.serialize import serialize_object

tool_type = types.Tool(
                name="Draft-Circle-FromCircularEdge",
                description="Create a labeled circle based on some circular edge in a named document",
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
                            "EdgeObjectLabel": {
                                "type": "string",
                                "description": "Name of the object the reference edge belongs to."
                            }, 
                            "EdgeIndex": {
                                "type": "integer",
                                "description": "Index of the reference edge in object shape."
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
    rpc_request_queue.put(lambda: _arc_by_center_radius_angles_gui(doc_name, label, probj))
    res, text = rpc_response_queue.get()
    return [types.TextContent(type="text", text=text)]

def _arc_by_center_radius_angles_gui(doc_name, label, probj):
    doc = FreeCAD.getDocument(doc_name)
    ref_obj = doc.getObjectsByLabel(probj.properties['EdgeObjectLabel'])[0]
    ref_curve = ref_obj.Shape.Edges[probj.properties['EdgeIndex']].Curve
    ref_rad = ref_curve.Radius
    ref_pos = ref_curve.Location
    circle = Draft.make_circle(ref_rad)
    rot = FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), 0)
    ctr = FreeCAD.Vector(0, 0, 0)
    circle.Placement = FreeCAD.Placement(ref_pos, rot, ctr)
    circle.Label = label
    doc.recompute()
    try:
        ser = serialize_object(circle)
    except Exception as e:
        return False, str(e)
    try:
        text = json.dumps(ser)
        return True, text
    except Exception as e:
        return False, str(e)
