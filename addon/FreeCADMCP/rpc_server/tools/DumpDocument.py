import mcp.types as types
import FreeCAD
import json
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue, Object
from rpc_server.serialize import serialize_object

tool_type =  types.Tool(
                name="DumpDocument",
                description="Create JSON dump of document",
                inputSchema={
                    "type": "object",
                    "required": ["Doc"],
                    "properties": {
                        "Doc": {
                            "type": "string",
                            "description": "Name of document to dump",
                        }
                    },
                },
            )

def do_it(args):
    doc_name = args.get('Doc')
    rpc_request_queue.put(lambda: _dump_document_gui(doc_name))
    res, text = rpc_response_queue.get()
    return [types.TextContent(type="text", text=text)]

def _dump_document_gui(doc_name):
    doc = FreeCAD.getDocument(doc_name)
    try:
        ser = serialize_object(doc)
    except Exception as e:
        FreeCAD.Console.PrintError(f"Document '{doc_name}' could not be serialized: '{str(e)}'.\n")
        return False, str(e)
    try:
        text = json.dumps(ser)
        return True, text
    except Exception as e:
        FreeCAD.Console.PrintError(f"Document '{doc_name}' could not be serialized: '{str(e)}'.\n")
        return False, str(e)