import mcp.types as types
import FreeCADGui
from sse_server.sse_server import sse_request_queue, sse_response_queue

tool_type = types.Tool(
                name="Std-ViewHome",
                description="Set default mode for active view",
                inputSchema={
                    "type": "object",
                    "required": [],
                    "properties": {}
                },
            )

def do_it(args):
    """Set default mode for the active view.
    """
                
    sse_request_queue.put(
        lambda: _set_home_view()
    )
    res = sse_response_queue.get()
    if res is True:
        return [types.textContent(type="text", text="ViewHome")]
    else:
        return [types.TextContent(type="text", text=res)]

def _set_home_view():
    try:
        view = FreeCADGui.ActiveDocument.ActiveView
        view.viewHome()
        return True
    except Exception as e:
        return str(e)
