import mcp.types as types
import FreeCADGui
from addon.FreeCADMCP.rcp_server.rpc_server import rcp_request_queue, rcp_response_queue

tool_type = types.Tool(
                name="Std-PerspectiveCamera",
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
                
    rcp_request_queue.put(
        lambda: _set_perspective_camera()
    )
    res = rcp_response_queue.get()
    if res is True:
        return [types.TextContent(type="text", text="PerspectiveCamera")]
    else:
        return [types.TextContent(type="text", text=res)]

def _set_perspective_camera():
    try:
        view = FreeCADGui.ActiveDocument.ActiveView
        view.setCameraType("Perspective")
        return True
    except Exception as e:
        return str(e)
