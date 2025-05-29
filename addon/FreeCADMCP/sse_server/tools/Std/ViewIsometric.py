import mcp.types as types
import FreeCADGui
from sse_server.sse_server import sse_request_queue, sse_response_queue

tool_type = types.Tool(
                name="Std-ViewIsometric",
                description="Set isometric mode for active view",
                inputSchema={
                    "type": "object",
                    "required": [],
                    "properties": {}
                },
            )

def do_it(args):
    """Set isometric mode for the active view.
    """
                
    sse_request_queue.put(
        lambda: _set_isometric_view()
    )
    res = sse_response_queue.get()
    if res is True:
        return [types.TextContent(type="text", text="ViewIsometric")]
    else:
        return [types.TextContent(type="text", text=res)]

def _set_isometric_view():
    try:
        view = FreeCADGui.ActiveDocument.ActiveView
        view.viewIsometric()
        return True
    except Exception as e:
        return str(e)
