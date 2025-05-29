import mcp.types as types
from sse_server.parts_library import get_parts_list

tool_type = types.Tool(
                name="Std-MergeProject-ListPartsLibrary",
                description="List the parts contained in the parts_library",
                inputSchema={
                    "type": "object",
                    "required": [],
                    "properties": {}
                },
            )

def do_it(args) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    result = []
    for p in get_parts_list():
        result.append(types.TextContent(type="text", text=p))
    return result
