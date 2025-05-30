import mcp.types as types
import FreeCADGui
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue

tool_type = types.Tool(
                name="Std-OrtographicCamera",
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
                
    rpc_request_queue.put(
        lambda: _set_orthographic_camera()
    )
    res = rpc_response_queue.get()
    if res is True:
        return [types.TextContent(type="text", text="OrthographicCamera")]
    else:
        return [types.TextContent(type="text", text=res)]

def _set_orthographic_camera():
    try:
        view = FreeCADGui.ActiveDocument.ActiveView
        view.setCameraType("Orthographic")
        return True
    except Exception as e:
        return str(e)
