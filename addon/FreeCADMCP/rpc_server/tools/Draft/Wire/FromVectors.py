import mcp.types as types
import FreeCAD
import Draft
import json
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue, Object
from rpc_server.serialize import serialize_object

tool_type = types.Tool(
                name="Draft-Wire-FromVectors",
                description="Create a labeled line object from vectors in a named document",
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
                            "Vectors": {
                                "type": "number",
                                "description": "List of vectors."
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
    doc_name = args.get("Doc")
    label = args.get("Label")
    obj = Object(
        name=label,
        properties=args.get("Properties", {}),
    )
    rpc_request_queue.put(lambda: _wire_from_points_gui(doc_name, label, obj))
    res, text = rpc_response_queue.get()
    return [types.TextContent(type="text", text=text)]

def _wire_from_points_gui(doc_name, label, obj):
    doc = FreeCAD.getDocument(doc_name)
    vectors = obj.properties["Vectors"]
    closed = None
    if "Closed" in obj.properties:
        closed = obj.properties["Closed"]
    face = None
    if closed and "Face" in obj.properties:
        face = obj.properties["Face"]
    vectorlist = []
    for v in vectors:
        vectorlist.append(FreeCAD.Vector(v))
    wire = Draft.make_wire(vectorlist, closed=closed, face=face)
    wire.Label = label
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