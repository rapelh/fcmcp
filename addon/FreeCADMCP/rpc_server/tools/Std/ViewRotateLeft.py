import mcp.types as types
import FreeCADGui
from addon.FreeCADMCP.rcp_server.rpc_server import rcp_request_queue, rcp_response_queue

tool_type = types.Tool(
                name="Std-ViewRotateLeft",
                description="Set rotateleft mode for active view",
                inputSchema={
                    "type": "object",
                    "required": [],
                    "properties": {}
                },
            )

def do_it(args):
    """Set rotateleft mode for the active view.
    """
                
    rcp_request_queue.put(
        lambda: _set_rotateleft_view()
    )
    res = rcp_response_queue.get()
    if res is True:
        return [types.TextContent(type="text", text="ViewRotateLeft")]
    else:
        return [types.TextContent(type="text", text=res)]

def _set_rotateleft_view():
    try:
        view = FreeCADGui.ActiveDocument.ActiveView
        view.viewRotateLeft()
        return True
    except Exception as e:
        return str(e)
