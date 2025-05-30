import mcp.types as types
import FreeCADGui
from addon.FreeCADMCP.rcp_server.rpc_server import rcp_request_queue, rcp_response_queue

tool_type = types.Tool(
                name="Std-SetStereoType",
                description="Set stereo type for active view",
                inputSchema={
                    "type": "object",
                    "required": [],
                    "properties": {
                        "Type": {
                            "type": "string",
                            "description": "Name of the stereo type to set",
                        }                        
                    }
                },
            )

def do_it(args):
    """Set stereo type for active view.
    """
    stereo_type = args.get('Type')
    if not stereo_type in ["Anaglyph", "QuadBuffer", "InterleavedRows", "InterleavedColumns", "None"]:
        return [types.TextContent(type="text", text=f"Unknown stereo type {stereo_type}")]
    rcp_request_queue.put(
        lambda: _set_stereo_type(stereo_type)
    )
    res = rcp_response_queue.get()
    if res is True:
        return [types.TextContent(type="text", text=stereo_type)]
    else:
        return [types.TextContent(type="text", text=res)]

def _set_stereo_type():
    try:
        view = FreeCADGui.ActiveDocument.ActiveView
        view.setStereoType("Anaglyph")
        return True
    except Exception as e:
        return str(e)
