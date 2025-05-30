import mcp.types as types
import FreeCADGui
from addon.FreeCADMCP.rcp_server.rpc_server import rcp_request_queue, rcp_response_queue

tool_type = types.Tool(
                name="Std-ViewRight",
                description="Set right mode for active view",
                inputSchema={
                    "type": "object",
                    "required": [],
                    "properties": {}
                },
            )

def do_it(args):
    """Set right mode for the active view.
    """
                
    rcp_request_queue.put(
        lambda: _set_right_view()
    )
    res = rcp_response_queue.get()
    if res is True:
        return [types.TextContent(type="text", text="ViewRight")]
    else:
        return [types.TextContent(type="text", text=res)]

def _set_right_view():
    try:
        view = FreeCADGui.ActiveDocument.ActiveView
        view.viewRight()
        return True
    except Exception as e:
        return str(e)
