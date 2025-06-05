import mcp.types as types
import FreeCAD
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue

tool_type = types.Tool(
                name="App-DocumentObject-Del",
                description="Delete a named object in a named document",
                inputSchema={
                    "type": "object",
                    "required": ["DocName", "ObjName"],
                    "properties": {
                        "DocName": {
                            "type": "string",
                            "description": "Name of document the object belongs to",
                        },
                        "ObjName": {
                            "type": "string",
                            "description": "Name of object to modify",
                        }
                    },
                },
            )

def do_it(args):
    doc_name = args.get('DocName')
    obj_name = args.get('ObjName')
    rpc_request_queue.put(lambda: _delete_object_gui(doc_name, obj_name))
    res, text = rpc_response_queue.get()
    if res is True:
        return [types.TextContent(type="text", text=text)]
    else:
        return [types.TextContent(type="text", text=res)]

def _delete_object_gui(doc_name: str, obj_name: str):
    doc = FreeCAD.getDocument(doc_name)
    if not doc:
        FreeCAD.Console.PrintError(f"Document '{doc_name}' not found.\n")
        return False, f"Document '{doc_name}' not found.\n"

    try:
        doc.removeObject(obj_name)
        doc.recompute()
        FreeCAD.Console.PrintMessage(f"Object '{obj_name}' deleted via RPC.\n")
        return True, f"{obj_name} deleted"
    except Exception as e:
        return False, str(e)
