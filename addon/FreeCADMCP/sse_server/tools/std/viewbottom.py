import mcp.types as types
import FreeCADGui
from sse_server.sse_server import sse_request_queue, sse_response_queue

tool_type = types.Tool(
                name="std-viewbottom",
                description="Set bottom mode for active view",
                inputSchema={
                    "type": "object",
                    "required": [],
                    "properties": {}
                },
            )

def do_it(args):
    """Set bottom mode for the active view.
    """
                
    sse_request_queue.put(
        lambda: _set_bottom_view()
    )
    res = sse_response_queue.get()
    if res is True:
        return [types.textContent(type="text", text="ViewBottom")]
    else:
        return [types.TextContent(type="text", text=res)]

def _set_bottom_view():
    try:
        view = FreeCADGui.ActiveDocument.ActiveView
        view.viewBottom()
        return True
    except Exception as e:
        return str(e)
