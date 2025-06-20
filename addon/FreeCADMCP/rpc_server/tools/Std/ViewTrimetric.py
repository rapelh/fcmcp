import mcp.types as types
import FreeCADGui
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue

tool_type = types.Tool(
                name="Std-ViewTrimetric",
                description="Set trimetric mode for active view",
                inputSchema={
                    "type": "object",
                    "required": [],
                    "properties": {}
                },
            )

def do_it(args):
    """Set trimetric mode for the active view.
    """
                
    rpc_request_queue.put(
        lambda: _set_trimetric_view()
    )
    res = rpc_response_queue.get()
    if res is True:
        return [types.TextContent(type="text", text="ViewTrimetric")]
    else:
        return [types.TextContent(type="text", text=res)]

def _set_trimetric_view():
    try:
        view = FreeCADGui.ActiveDocument.ActiveView
        view.viewTrimetric()
        return True
    except Exception as e:
        return str(e)
