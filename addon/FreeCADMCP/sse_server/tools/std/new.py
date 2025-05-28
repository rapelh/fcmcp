import mcp.types as types
import FreeCAD
from sse_server.sse_server import sse_request_queue
from sse_server.sse_server import sse_response_queue

tool_type = types.Tool(
                name="std-new",
                description="Create a named document and returns its name",
                inputSchema={
                    "type": "object",
                    "required": ["name"],
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name of document to create",
                        }
                    },
                },
            )


def do_it(args):
    print('Std New in FreeCADSSE create_document', args)
    sse_request_queue.put(lambda: _create_document_gui(args['name']))
    res = sse_response_queue.get()
    if res is True:
        return [types.TextContent(type="text", text=args['name'])]
    else:
        return [types.TextContent(type="text", text=res)]

def _create_document_gui(name):
    print('Std New in FreeCADSSE _create_document_gui')
    doc = FreeCAD.newDocument(name)
    doc.recompute()
    FreeCAD.Console.PrintMessage(f"Document '{name}' created via SSE.\n")
    return True