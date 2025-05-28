import mcp.types as types
import FreeCADGui
from sse_server.sse_server import sse_request_queue, sse_response_queue

tool_type = types.Tool(
                name="std-viewfitselection",
                description="Set fitselection for active view",
                inputSchema={
                    "type": "object",
                    "required": [],
                    "properties": {}
                },
            )

def do_it(args):
    """
    Set fitselection for the active view.
    """
                
    sse_request_queue.put(
        lambda: _set_fitselection_view()
    )
    res = sse_response_queue.get()
    if res is True:
        return [types.textContent(type="text", text="ViewFitSelection")]
    else:
        return [types.TextContent(type="text", text=res)]

def _set_fitselection_view():
    try:
        FreeCADGui.SendMsgToActiveView("ViewSelection")
        return True
    except Exception as e:
        return str(e)
