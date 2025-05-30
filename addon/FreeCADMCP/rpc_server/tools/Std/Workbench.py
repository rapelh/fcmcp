import mcp.types as types
import FreeCADGui
from addon.FreeCADMCP.rcp_server.rpc_server import rcp_request_queue, rcp_response_queue

tool_type = types.Tool(
                name="Std-Workbench",
                description="Toggle visibility of named object in a named document",
                inputSchema={
                    "type": "object",
                    "required": ["Name"],
                    "properties": {
                        "Name": {
                            "type": "string",
                            "description": "Name of object to create",
                        },
                    },
                },
            )

def do_it(args):
    wb_name = args.get("Name")
    rcp_request_queue.put(lambda: _activate_workbench_gui(wb_name))
    res = rcp_response_queue.get()
    if res is True:
        return [types.TextContent(type="text", text=wb_name)]
    else:
        return [types.TextContent(type="text", text=res)]

def _activate_workbench_gui(wb_name: str):
    try:
        FreeCADGui.activateWorkbench(wb_name)
        return True
    except Exception as e:
        return str(e)