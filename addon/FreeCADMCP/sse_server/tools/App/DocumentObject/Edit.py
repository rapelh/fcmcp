import mcp.types as types
import FreeCAD
from sse_server.sse_server import sse_request_queue, sse_response_queue, set_object_property, Object

tool_type = types.Tool(
                name="App-DocumentObject-Edit",
                description="Modify properties of a named object in a named document",
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
                        },
                        "Length": {
                            "type": "float",
                            "description": "Length of object to set",
                        },
                        "Width": {
                            "type": "float",
                            "description": "Width of object to set",
                        },
                        "Height": {
                            "type": "float",
                            "description": "Height of object to set",
                        },
                        "Radius": {
                            "type": "float",
                            "description": "Radius of object to set",
                        }
                    },
                },
            )
# def edit_object(self, doc_name: str, obj_name: str, properties: dict[str, Any]) -> dict[str, Any]:
def do_it(args):
    doc_name = args.get('Doc')
    obj_name = args.get('Name')
    obj = Object(
        name=obj_name,
        properties=args.get("Properties", {}),
    )
    sse_request_queue.put(lambda: _edit_object_gui(doc_name, obj))
    res = sse_response_queue.get()
    if res is True:
        return [types.TextContent(type="text", text=obj.name)]
    else:
        return [types.TextContent(type="text", text=res)]

def _edit_object_gui(doc_name: str, obj: Object):
    doc = FreeCAD.getDocument(doc_name)
    if not doc:
        FreeCAD.Console.PrintError(f"Document '{doc_name}' not found.\n")
        return f"Document '{doc_name}' not found.\n"

    obj_ins = doc.getObject(obj.name)
    if not obj_ins:
        FreeCAD.Console.PrintError(f"Object '{obj.name}' not found in document '{doc_name}'.\n")
        return f"Object '{obj.name}' not found in document '{doc_name}'.\n"

    try:
        # For Fem::ConstraintFixed
        if hasattr(obj_ins, "References") and "References" in obj.properties:
            refs = []
            for ref_name, face in obj.properties["References"]:
                ref_obj = doc.getObject(ref_name)
                if ref_obj:
                    refs.append((ref_obj, face))
                else:
                    raise ValueError(f"Referenced object '{ref_name}' not found.")
            obj_ins.References = refs
            FreeCAD.Console.PrintMessage(
                f"References updated for '{obj.name}' in '{doc_name}'.\n"
            )
            # delete References from properties
            del obj.properties["References"]
        set_object_property(doc, obj_ins, obj.properties)
        doc.recompute()
        FreeCAD.Console.PrintMessage(f"Object '{obj.name}' updated via SSE.\n")
        return True
    except Exception as e:
        return str(e)
