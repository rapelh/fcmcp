import mcp.types as types
import FreeCADGui
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue

tool_type = types.Tool(
                name="Std-ViewFront",
                description="Set front mode for active view",
                inputSchema={
                    "type": "object",
                    "required": [],
                    "properties": {}
                },
            )

def do_it(args):
    """Set front mode for the active view.
    """
                
    rpc_request_queue.put(
        lambda: _set_front_view()
    )
    res = rpc_response_queue.get()
    if res is True:
        return [types.TextContent(type="text", text="ViewFront")]
    else:
        return [types.TextContent(type="text", text=res)]

def _set_front_view():
    try:
        view = FreeCADGui.ActiveDocument.ActiveView
        view.viewFront()
        return True
    except Exception as e:
        return str(e)
