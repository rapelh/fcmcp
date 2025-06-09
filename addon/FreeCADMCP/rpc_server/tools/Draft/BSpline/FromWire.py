import mcp.types as types
import FreeCAD
import Draft
import Part
import json
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue, Object
from rpc_server.serialize import serialize_object

tool_type = types.Tool(
                name="Draft-BSpline-FromWire",
                description="Create a labeled bspline object from a wire in a named document",
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
                            "WireName": {
                                "type": "string",
                                "description": "Name of reference object whos shape is the reference wire."
                            },
                            "Closed": {
                                "type": "boolean",
                                "description": "Close the wire."
                            },
                            "Face": {
                                "type": "boolean",
                                "description": "Try to create a face from a closed wire."
                            } 
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
    rpc_request_queue.put(lambda: _bspline_from_wire_gui(doc_name, label, probj))
    res, text = rpc_response_queue.get()
    return [types.TextContent(type="text", text=text)]

def _bspline_from_wire_gui(doc_name, label, probj):
    doc = FreeCAD.getDocument(doc_name)
    obj = doc.getObject(probj.properties["WireName"])
    wire = obj.Shape
    closed = None
    if "Closed" in probj.properties:
        closed = probj.properties["Closed"]
    face = None
    if closed and "Face" in probj.properties:
        face = probj.properties["Face"]
    bspline = Draft.make_bspline(wire, closed=closed, face=face)
    bspline.Label = label
    doc.recompute()
    try:
        ser = serialize_object(bspline)
    except Exception as e:
        return False, str(e)
    try:
        text = json.dumps(ser)
        return True, text
    except Exception as e:
        return False, str(e)