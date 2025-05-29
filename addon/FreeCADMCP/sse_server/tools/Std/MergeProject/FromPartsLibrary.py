import mcp.types as types
import FreeCAD
from sse_server.sse_server import sse_request_queue, sse_response_queue
from sse_server.parts_library import get_parts_list, insert_part_from_library

tool_type = types.Tool(
                name="Std-MergeProject-FromPartsLibrary",
                description="Insert part from parts library",
                inputSchema={
                    "type": "object",
                    "required": ["RelativePath"],
                    "properties": {
                        "RelativePath": {
                            "type": "string",
                            "description": "Relative path in part library",
                        }
                    },
                },
            )

# def insert_part_from_library(self, relative_path):
def do_it(args):
    relative_path = args.get('RelativePath')
    sse_request_queue.put(lambda: _insert_part_from_library(relative_path))
    res = sse_response_queue.get()
    if res is True:
        return [types.TextContent(type="text", text=relative_path)]
    else:
        return [types.TextContent(type="text", text=res)]


def _insert_part_from_library(relative_path):
    try:
        insert_part_from_library(relative_path)
        return True
    except Exception as e:
        return str(e)