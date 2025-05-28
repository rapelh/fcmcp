import mcp.types as types
import FreeCADGui
from sse_server.sse_server import sse_request_queue, sse_response_queue

tool_type = types.Tool(
                name="std-ortographiccamera",
                description="Set orthographic camera for active view",
                inputSchema={
                    "type": "object",
                    "required": [],
                    "properties": {}
                },
            )

def do_it(args):
    """Set orthographic camera for the active view.
    """
                
    sse_request_queue.put(
        lambda: _set_orthographic_camera()
    )
    res = sse_response_queue.get()
    if res is True:
        return [types.textContent(type="text", text="OrthographicCamera")]
    else:
        return [types.TextContent(type="text", text=res)]

def _set_orthographic_camera():
    try:
        view = FreeCADGui.ActiveDocument.ActiveView
        view.setCameraType("Orthographic")
        return True
    except Exception as e:
        return str(e)
