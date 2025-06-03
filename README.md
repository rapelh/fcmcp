# fcmcp
## MCP for FreeCAD 1.0+

A MCP server as addon for FreeCAD 1.0+ with Streamable HTTP transport, based on https://github.com/modelcontextprotocol/python-sdk.

With ideas taken from:
- https://github.com/neka-nat/freecad-mcp
- https://github.com/zanetworker/mcp-sse-client-python
- https://github.com/golf-mcp/golf

Additional tools may be added to addon/FreeCADMCP/sse_server/tools following the examples and these are automatically loaded into the server.

### Installation

- Locate your FreeCAD local personal home directory:
-- For a Snap installation, ~/snap/freecad/ 
-- For an AppImage execution: ~/.local/share/FreeCAD/
- Make sure a folder ./Mod/ exists below

On Ubuntu, copy the folder addon/FreeCADMCP to that ./Mod/ folder and restart FreeCAD.

In FreeCAD, select the workbench "MCP addon" and setup the MCP server with the command button labeled "Init RPC Server".

After restarting FreeCAD again and again selecting the "MCP addon" workbench, there will be 3 command buttons available: 
- "Start RPC Server"
- "Stop RPC Server"
- "Init RPC Server"


### Usage

In FreeCAD, select the workbench "MCP addon". 

Start the MCP server with the button labeled "Start RPC Server"

The test*.py scripts provide examples of tool invocation.

Under ./agents/ several examples of FreeCAD-MCP agents have been collected.