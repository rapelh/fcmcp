import mcp.types as types
import FreeCADGui
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue

tool_type = types.Tool(
                name="Std-ViewRotateRight",
                description="Set rotateright mode for active view",
                inputSchema={
                    "type": "object",
                    "required": [],
                    "properties": {}
                },
            )

def do_it(args):
    """Set rotateright mode for the active view.
    """

    rpc_request_queue.put(
        lambda: _set_rotateright_view()
    )
    res = rpc_response_queue.get()
    if res is True:
        return [types.TextContent(type="text", text="ViewRotateRight")]
    else:
        return [types.TextContent(type="text", text=res)]

def _set_rotateright_view():
    try:
        view = FreeCADGui.ActiveDocument.ActiveView
        view.viewRotateRight()
        return True
    except Exception as e:
        return str(e)
