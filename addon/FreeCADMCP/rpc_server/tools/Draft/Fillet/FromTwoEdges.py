import mcp.types as types
import FreeCAD
import Draft
import json
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue, Object
from rpc_server.serialize import serialize_object

tool_type = types.Tool(
                name="Draft-Fillet-FromTwoEdges",
                description="Create a labeled line object from vectors in a named document",
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
                            "description": "Name of object to get edges from",
                        },
                        "Properties": {
                            "Label": {
                                "type": "string",
                                "description": "Label of fillet to create"
                            }, 
                            "EdgeIndex1": {
                                "type": "integer",
                                "description": "Index of first edge in Shape.Edges of named object"
                            }, 
                            "EdgeIndex2": {
                                "type": "integer",
                                "description": "Index of first edge in Shape.Edges of named object"
                            }, 
                            "Radius": {
                                "type": "number",
                                "description": "Radius of the fillet to create"
                            }, 
                        },
                    },
                },
            )

def do_it(args):
    doc_name = args.get("DocName")
    obj_name = args.get("ObjName")
    probj = Object(
        name=obj_name,
        properties=args.get("Properties", {}),
    )
    rpc_request_queue.put(lambda: _fillet_from_two_edges_gui(doc_name, obj_name, probj))
    res, text = rpc_response_queue.get()
    return [types.TextContent(type="text", text=text)]

def _fillet_from_two_edges_gui(doc_name, obj_name, probj):
    doc = FreeCAD.getDocument(doc_name)
    e1 = doc.getObject(obj_name).Shape.Edges[probj.properties["EdgeIndex1"]]
    e2 = doc.getObject(obj_name).Shape.Edges[probj.properties["EdgeIndex2"]]
    fillet = Draft.make_fillet([e1, e2], radius=probj.properties["Radius"])
    fillet.Label = probj.properties["Label"]
    doc.recompute()
    try:
        ser = serialize_object(fillet)
    except Exception as e:
        return False, str(e)
    try:
        text = json.dumps(ser)
        return True, text
    except Exception as e:
        return False, str(e)
