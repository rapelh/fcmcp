import mcp.types as types
import FreeCADGui
from sse_server.sse_server import sse_request_queue, sse_response_queue

tool_type = types.Tool(
                name="std-perspectivecamera",
                description="Set perspective camera for active view",
                inputSchema={
                    "type": "object",
                    "required": [],
                    "properties": {}
                },
            )

def do_it(args):
    """Set perspective camera for the active view.
    """
                
    sse_request_queue.put(
        lambda: _set_perspective_camera()
    )
    res = sse_response_queue.get()
    if res is True:
        return [types.textContent(type="text", text="PerspectiveCamera")]
    else:
        return [types.TextContent(type="text", text=res)]

def _set_orthographic_camera():
    try:
        view = FreeCADGui.ActiveDocument.ActiveView
        view.setCameraType("Perspective")
        return True
    except Exception as e:
        return str(e)
