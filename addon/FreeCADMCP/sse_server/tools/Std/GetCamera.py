import mcp.types as types
import FreeCADGui
from sse_server.sse_server import sse_request_queue, sse_response_queue

tool_type = types.Tool(
                name="Std-GetCamera",
                description="Get active 3D view camera settings",
                inputSchema={
                    "type": "object",
                    "required": [],
                    "properties": {}
                },
            )

def do_it(args):
    """Get active 3D view camera settings.
    """
                
    sse_request_queue.put(
        lambda: _get_camera()
    )
    res, settings = sse_response_queue.get()
    if res is True:
        return [types.textContent(type="text", text=settings)]
    else:
        return [types.TextContent(type="text", text=res)]

def _get_camera():
    try:
        view = FreeCADGui.ActiveDocument.ActiveView
        settings = view.getCamera()
        return True, settings
    except Exception as e:
        return str(e)
