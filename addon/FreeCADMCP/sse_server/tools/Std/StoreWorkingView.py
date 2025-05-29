import mcp.types as types
import FreeCADGui
from sse_server.sse_server import sse_request_queue, sse_response_queue

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
                
    sse_request_queue.put(
        lambda: _store_working_view()
    )
    res = sse_response_queue.get()
    if res is True:
        return [types.textContent(type="text", text="StoreWorkingView")]
    else:
        return [types.TextContent(type="text", text=res)]

def _store_working_view():
    try:
        FreeCADGui.runCommand("Std_StoreWorkingView", 0)
        return True
    except Exception as e:
        return str(e)
