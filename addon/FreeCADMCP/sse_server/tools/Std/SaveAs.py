import mcp.types as types
import FreeCAD
from sse_server.sse_server import sse_request_queue
from sse_server.sse_server import sse_response_queue

tool_type = types.Tool(
                name="Std-SaveAs",
                description="Save a document to a file",
                inputSchema={
                    "type": "object",
                    "required": ["Doc", "Path"],
                    "properties": {
                        "Doc": {
                            "type": "string",
                            "description": "Document name",
                        },
                        "Path": {
                            "type": "string",
                            "description": "Path to save the document to",
                        }
                    },
                },
            )


def do_it(args):
    doc_name = args.get('Doc')
    path = args.get('Path')
    sse_request_queue.put(lambda: _saveas_document_gui(doc_name, path))
    res = sse_response_queue.get()
    if res is True:
        return [types.TextContent(type="text", text=path)]
    else:
        return [types.TextContent(type="text", text=res)]

def _saveas_document_gui(doc_name, path):
    doc = FreeCAD.getDocument(doc_name)
    doc.saveAs(path)
    FreeCAD.Console.PrintMessage(f"Document '{doc.Name}' saved to from {path}.\n")
    return True