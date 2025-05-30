import mcp.types as types
import FreeCAD
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue

tool_type = types.Tool(
                name="Std-Open",
                description="Open a document file",
                inputSchema={
                    "type": "object",
                    "required": ["Path"],
                    "properties": {
                        "Path": {
                            "type": "string",
                            "description": "Path document to open",
                        }
                    },
                },
            )


def do_it(args):
    path = args.get('Path')
    rpc_request_queue.put(lambda: _open_document_gui(path))
    res = rpc_response_queue.get()
    if res is True:
        return [types.TextContent(type="text", text=path)]
    else:
        return [types.TextContent(type="text", text=res)]

def _open_document_gui(path):
    doc = FreeCAD.open(path)
    doc.recompute()
    FreeCAD.Console.PrintMessage(f"Document '{doc.Name}' opened from {path}.\n")
    return True