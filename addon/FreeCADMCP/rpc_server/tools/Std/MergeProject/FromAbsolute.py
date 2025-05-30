import mcp.types as types
import FreeCAD
from addon.FreeCADMCP.rcp_server.rpc_server import rcp_request_queue, rcp_response_queue

tool_type = types.Tool(
                name="Std-MergeProject-FromAbsolute",
                description="Insert part from absolute location",
                inputSchema={
                    "type": "object",
                    "required": ["AbsolutePath"],
                    "properties": {
                        "AbsolutePath": {
                            "type": "string",
                            "description": "Absolute path in part library",
                        }
                    },
                },
            )

def do_it(args):
    absolute_path = args.get('AbsolutePath')
    rcp_request_queue.put(lambda: _insert_part_from_absolute(absolute_path))
    res = rcp_response_queue.get()
    if res is True:
        return [types.TextContent(type="text", text=absolute_path)]
    else:
        return [types.TextContent(type="text", text=res)]


def _insert_part_from_absolute(absolute_path):
    try:
        FreeCAD.ActiveDocument.mergeProject(absolute_path)
        return True
    except Exception as e:
        return str(e)