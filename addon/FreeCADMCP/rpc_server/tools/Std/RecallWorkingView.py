import mcp.types as types
import FreeCADGui
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue

tool_type = types.Tool(
                name="Std-RecallWorkingView",
                description="Recall working view as mode for active view",
                inputSchema={
                    "type": "object",
                    "required": [],
                    "properties": {}
                },
            )

def do_it(args):
    """Recall working view as mode for active view.
    """
                
    rpc_request_queue.put(
        lambda: _recall_working_view()
    )
    res = rpc_response_queue.get()
    if res is True:
        return [types.TextContent(type="text", text="RecallWorkingView")]
    else:
        return [types.TextContent(type="text", text=res)]

def _recall_working_view():
    try:
        FreeCADGui.runCommand("Std_RecallWorkingView", 0)
        return True
    except Exception as e:
        return str(e)
