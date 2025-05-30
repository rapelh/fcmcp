import mcp.types as types
import FreeCADGui
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue

tool_type = types.Tool(
                name="Std-ViewZoomOut",
                description="Zoom out active view",
                inputSchema={
                    "type": "object",
                    "required": [],
                    "properties": {}
                },
            )

def do_it(args):
    """Zoom out active view.
    """
                
    rpc_request_queue.put(
        lambda: _zoom_out_view()
    )
    res = rpc_response_queue.get()
    if res is True:
        return [types.TextContent(type="text", text="ViewZoomOut")]
    else:
        return [types.TextContent(type="text", text=res)]

def _zoom_out_view():
    try:
        view = FreeCADGui.ActiveDocument.ActiveView
        view.viewZoomOut()
        return True
    except Exception as e:
        return str(e)
