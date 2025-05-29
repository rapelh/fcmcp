import mcp.types as types
import FreeCAD
from sse_server.sse_server import sse_request_queue, sse_response_queue

tool_type = types.Tool(
                name="Std-ToggleVisibility",
                description="Toggle visibility of named object in a named document",
                inputSchema={
                    "type": "object",
                    "required": ["Doc", "Name"],
                    "properties": {
                        "Doc": {
                            "type": "string",
                            "description": "Name of document in which to create",
                        },
                        "Name": {
                            "type": "string",
                            "description": "Name of object to create",
                        },
                    },
                },
            )

def do_it(args):
    doc_name = args.get("Doc")
    obj_name = args.get("Name")
    sse_request_queue.put(lambda: _toggle_visibility_gui(doc_name, obj_name))
    res = sse_response_queue.get()
    if res is True:
        return [types.TextContent(type="text", text=obj_name)]
    else:
        return [types.TextContent(type="text", text=res)]

def _toggle_visibility_gui(doc_name: str, obj_name: str):
    doc = FreeCAD.getDocument(doc_name)
    if not doc:
        FreeCAD.Console.PrintError(f"Document '{doc_name}' not found.\n")
        return f"Document '{doc_name}' not found.\n"
    obj = doc.getObject(obj_name)
    if not obj:
        FreeCAD.Console.PrintError(f"Object '{obj_name}' not found in document '{doc_name}'.\n")
        return f"Object '{obj_name}' not found in document '{doc_name}'.\n"
    view_obj = obj.ViewObject
    try:
        view_obj.Visibility = not view_obj.Visibility
        return True
    except Exception as e:
        return str(e)