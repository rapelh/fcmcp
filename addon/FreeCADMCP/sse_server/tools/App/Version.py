import mcp.types as types
import FreeCAD

tool_type = types.Tool(
                name="App-Version",
                description="Fetches the FreeCAD version and returns its content",
                inputSchema={
                    "type": "object",
                    "required": [],
                    "properties": {}
                },
            )

def do_it(args) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    result = []
    print(FreeCAD.Version())
    result.append(types.TextContent(type="text", text=" ".join(FreeCAD.Version())))
    return result
