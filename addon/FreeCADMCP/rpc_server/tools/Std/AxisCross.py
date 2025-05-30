import mcp.types as types
import FreeCADGui
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue

tool_type = types.Tool(
                name="Std-AxisCross",
                description="Set or unset axis cross in active view",
                inputSchema={
                    "type": "object",
                    "required": [],
                    "properties": {
                        "Activate": {
                            "type": "bool",
                            "description": "Activate or deactivate",
                        }
                    }
                },
            )

def do_it(args):
    """Set or unset axis cross in active view.
    """
    activate = args.get('Activate')           
    rpc_request_queue.put(
        lambda: _set_axiscross(activate)
    )
    res = rpc_response_queue.get()
    if res is True:
        return [types.TextContent(type="text", text="AxisCross "+activate)]
    else:
        return [types.TextContent(type="text", text=res)]

def _set_axiscross(activate):
    try:
        view = FreeCADGui.ActiveDocument.ActiveView
        view.setAxisCross(activate)
        return True
    except Exception as e:
        return str(e)
