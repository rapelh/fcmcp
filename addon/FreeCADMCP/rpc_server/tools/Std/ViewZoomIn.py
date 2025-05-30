import mcp.types as types
import FreeCADGui
from addon.FreeCADMCP.rcp_server.rpc_server import rcp_request_queue, rcp_response_queue

tool_type = types.Tool(
                name="Std-ViewZoomIn",
                description="Zoom in active view",
                inputSchema={
                    "type": "object",
                    "required": [],
                    "properties": {}
                },
            )

def do_it(args):
    """Zoom in active view.
    """
                
    rcp_request_queue.put(
        lambda: _zoom_in_view()
    )
    res = rcp_response_queue.get()
    if res is True:
        return [types.TextContent(type="text", text="ViewZoomIn")]
    else:
        return [types.TextContent(type="text", text=res)]

def _zoom_in_view():
    try:
        view = FreeCADGui.ActiveDocument.ActiveView
        view.viewZoomIn()
        return True
    except Exception as e:
        return str(e)
