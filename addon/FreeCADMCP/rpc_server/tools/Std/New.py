import mcp.types as types
import FreeCAD
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue

tool_type = types.Tool(
                name="Std-New",
                description="Create a named document and returns its name",
                inputSchema={
                    "type": "object",
                    "required": ["Name"],
                    "properties": {
                        "Name": {
                            "type": "string",
                            "description": "Name of document to create",
                        }
                    },
                },
            )


def do_it(args):
    name = args.get('Name')
    rpc_request_queue.put(lambda: _create_document_gui(name))
    res, text = rpc_response_queue.get()
    if res is True:
        return [types.TextContent(type="text", text=text)]
    else:
        return [types.TextContent(type="text", text=text)]

def _create_document_gui(name):
    doc = FreeCAD.newDocument(name)
    doc.recompute()
    FreeCAD.Console.PrintMessage(f"Document '{name}' created via RPC.\n")
    return True, f"{name} created"