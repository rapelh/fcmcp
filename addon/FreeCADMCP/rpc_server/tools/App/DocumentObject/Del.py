import mcp.types as types
import FreeCAD
from addon.FreeCADMCP.rpc_server.rpc_server import rpc_request_queue, rpc_response_queue

tool_type = types.Tool(
                name="App-DocumentObject-Del",
                description="Delete a named object in a named document",
                inputSchema={
                    "type": "object",
                    "required": ["Doc", "Name"],
                    "properties": {
                        "Doc": {
                            "type": "string",
                            "description": "Name of document the object belongs to",
                        },
                        "Name": {
                            "type": "string",
                            "description": "Name of object to modify",
                        }
                    },
                },
            )

# def delete_object(doc_name: str, obj_name: str):
def do_it(args):
    doc_name = args.get('Doc')
    obj_name = args.get('Name')
    rpc_request_queue.put(lambda: _delete_object_gui(doc_name, obj_name))
    res = rpc_response_queue.get()
    if res is True:
        return [types.TextContent(type="text", text=obj_name)]
    else:
        return [types.TextContent(type="text", text=res)]

def _delete_object_gui(doc_name: str, obj_name: str):
    doc = FreeCAD.getDocument(doc_name)
    if not doc:
        FreeCAD.Console.PrintError(f"Document '{doc_name}' not found.\n")
        return f"Document '{doc_name}' not found.\n"

    try:
        doc.removeObject(obj_name)
        doc.recompute()
        FreeCAD.Console.PrintMessage(f"Object '{obj_name}' deleted via SSE.\n")
        return True
    except Exception as e:
        return str(e)
