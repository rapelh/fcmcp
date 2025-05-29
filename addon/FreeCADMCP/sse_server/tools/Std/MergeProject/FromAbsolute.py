import mcp.types as types
import FreeCAD
from sse_server.sse_server import sse_request_queue, sse_response_queue
from sse_server.parts_library import get_parts_list, insert_part_from_library

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
    sse_request_queue.put(lambda: _insert_part_from_absolute(absolute_path))
    res = sse_response_queue.get()
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