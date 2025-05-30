import mcp.types as types
import FreeCADGui
from addon.FreeCADMCP.rcp_server.rpc_server import rcp_request_queue, rcp_response_queue

tool_type = types.Tool(
                name="Std-StoreWorkingView",
                description="Store mode of active view as working view",
                inputSchema={
                    "type": "object",
                    "required": [],
                    "properties": {}
                },
            )

def do_it(args):
    """Store mode of active view as working view.
    """
                
    rcp_request_queue.put(
        lambda: _store_working_view()
    )
    res = rcp_response_queue.get()
    if res is True:
        return [types.TextContent(type="text", text="StoreWorkingView")]
    else:
        return [types.TextContent(type="text", text=res)]

def _store_working_view():
    try:
        FreeCADGui.runCommand("Std_StoreWorkingView", 0)
        return True
    except Exception as e:
        return str(e)
