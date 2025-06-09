import mcp.types as types
import FreeCAD
import Draft
import json
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue, Object
from rpc_server.serialize import serialize_object

tool_type = types.Tool(
                name="Draft-Arc-ByCenterRadiusAngles",
                description="Create a labeled arc object from center and radius in a named document",
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
                            "Center": {
                                "X": {
                                    "type": "number",
                                    "description": "X coordinate of the center vector. Default 0mm."
                                }, 
                                "Y": {
                                    "type": "number",
                                    "description": "Y coordinate of the center vector. Default 0mm."
                                }, 
                                "Z": {
                                    "type": "number",
                                    "description": "Z coordinate of the center vector. Default 0mm."
                                }, 
                            },
                            "StartAngle": {
                                "type": "number",
                                "description": "Start angle of the arc."
                            }, 
                            "EndAngle": {
                                "type": "number",
                                "description": "End angle of the arc."
                            }, 
                            "Radius": {
                                "type": "number",
                                "description": "Radius of the arc. Default 10mm."
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
    ctr = FreeCAD.Vector(0, 0, 0)
    pos = FreeCAD.Vector(0, 0, 0)
    position = probj.properties["Center"]
    if position:
        pos[0] = position["X"]
        pos[1] = position["Y"]
        pos[2] = position["Z"]
    arc = Draft.make_circle(probj.properties["Radius"], startangle=probj.properties["StartAngle"], endangle=probj.properties["EndAngle"])
    rot = FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), 0)
    arc.Placement = FreeCAD.Placement(pos, rot, ctr)
    arc.Label = label
    doc.recompute()
    try:
        ser = serialize_object(arc)
    except Exception as e:
        return False, str(e)
    try:
        text = json.dumps(ser)
        return True, text
    except Exception as e:
        return False, str(e)
