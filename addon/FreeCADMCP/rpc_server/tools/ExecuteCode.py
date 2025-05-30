import mcp.types as types
import FreeCAD
import contextlib
import io
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue

tool_type =  types.Tool(
                name="ExecuteCode",
                description="Execute code text",
                inputSchema={
                    "type": "object",
                    "required": ["Code"],
                    "properties": {
                        "Code": {
                            "type": "string",
                            "description": "Text of code to execute",
                        }
                    },
                },
            )

#def execute_code(self, code: str) -> dict[str, Any]:
def do_it(args):
    code = args.get('Code')
    output_buffer = io.StringIO()
    def task():
        try:
            with contextlib.redirect_stdout(output_buffer):
                exec(code, globals())
            FreeCAD.Console.PrintMessage("Python code executed successfully.\n")
            return True
        except Exception as e:
            FreeCAD.Console.PrintError(
                f"Error executing Python code: {e}\n"
            )
            return f"Error executing Python code: {e}\n"

    rpc_request_queue.put(task)
    res = rpc_response_queue.get()
    if res is True:
        message = "Python code execution scheduled. \nOutput: " + output_buffer.getvalue()
        return [types.TextContent(type="text", text=message)]
    else:
        return [types.TextContent(type="text", text=res)]
