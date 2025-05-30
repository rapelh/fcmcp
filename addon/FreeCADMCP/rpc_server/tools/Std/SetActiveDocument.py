import mcp.types as types
import FreeCAD
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue

tool_type = types.Tool(
                name="Std-SetActiveDocument",
                description="Set a named document as the active one",
                inputSchema={
                    "type": "object",
                    "required": ["Doc"],
                    "properties": {
                        "Doc": {
                            "type": "string",
                            "description": "Name of document to make active",
                        }
                    },
                },
            )


def do_it(args):
    doc_name = args.get('Doc')
    rpc_request_queue.put(lambda: _set_active_document_gui(doc_name))
    res = rpc_response_queue.get()
    if res is True:
        return [types.TextContent(type="text", text=doc_name)]
    else:
        return [types.TextContent(type="text", text=res)]

def _set_active_document_gui(doc_name):
    doc = FreeCAD.getDocument(doc_name)
    FreeCAD.setActiveDocument(doc_name)
    doc.recompute()
    FreeCAD.Console.PrintMessage(f"Document '{doc_name}' made active.\n")
    return True