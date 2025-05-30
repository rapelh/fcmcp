import mcp.types as types
import FreeCAD
from addon.FreeCADMCP.rcp_server.rpc_server import rcp_request_queue, rcp_response_queue
from rcp_server.parts_library import insert_part_from_library

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
    rcp_request_queue.put(lambda: _insert_part_from_library(relative_path))
    res = rcp_response_queue.get()
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