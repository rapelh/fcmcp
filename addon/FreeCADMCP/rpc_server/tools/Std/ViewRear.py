import mcp.types as types
import FreeCADGui
from addon.FreeCADMCP.rcp_server.rpc_server import rcp_request_queue, rcp_response_queue

tool_type = types.Tool(
                name="Std-ViewRear",
                description="Set rear mode for active view",
                inputSchema={
                    "type": "object",
                    "required": [],
                    "properties": {}
                },
            )

def do_it(args):
    """Set rear mode for the active view.
    """
                
    rcp_request_queue.put(
        lambda: _set_rear_view()
    )
    res = rcp_response_queue.get()
    if res is True:
        return [types.TextContent(type="text", text="ViewRear")]
    else:
        return [types.TextContent(type="text", text=res)]

def _set_rear_view():
    try:
        view = FreeCADGui.ActiveDocument.ActiveView
        view.viewRear()
        return True
    except Exception as e:
        return str(e)
