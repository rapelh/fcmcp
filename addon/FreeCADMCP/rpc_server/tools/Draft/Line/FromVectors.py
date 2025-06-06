import mcp.types as types
import FreeCAD
import Draft
import json
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue, Object
from rpc_server.serialize import serialize_object

tool_type = types.Tool(
                name="Draft-Line-FromVectors",
                description="Create a labeled line object from vectors in a named document",
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
                            "X1": {
                                "type": "number",
                                "description": "X coordinate of the first vector. Default 0mm."
                            }, 
                            "Y1": {
                                "type": "number",
                                "description": "Y coordinate of the first vector. Default 0mm."
                            }, 
                            "Z1": {
                                "type": "number",
                                "description": "Z coordinate of the first vector. Default 0mm."
                            }, 
                            "X2": {
                                "type": "number",
                                "description": "X coordinate of the second vector. Default 10mm."
                            }, 
                            "Y2": {
                                "type": "number",
                                "description": "Y coordinate of the second vector. Default 10mm."
                            }, 
                            "Z2": {
                                "type": "number",
                                "description": "Z coordinate of the second vector. Default 10mm."
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
    rpc_request_queue.put(lambda: _line_from_vectors_gui(doc_name, label, probj))
    res, text = rpc_response_queue.get()
    return [types.TextContent(type="text", text=text)]

def _line_from_vectors_gui(doc_name, label, probj):
    doc = FreeCAD.getDocument(doc_name)
    p1 = FreeCAD.Vector(probj.properties["X1"], probj.properties["Y1"], probj.properties["Z1"])
    p2 = FreeCAD.Vector(probj.properties["X2"], probj.properties["Y2"], probj.properties["Z2"])
    line = Draft.make_line(p1, p2)
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
