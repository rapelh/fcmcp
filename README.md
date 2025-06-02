# fcmcp
## MCP for FreeCAD 1.0+

A MCP server as addon for FreeCAD 1.0+ with Streamable HTTP transport, based on https://github.com/modelcontextprotocol/python-sdk.

With ideas taken from:
- https://github.com/neka-nat/freecad-mcp
- https://github.com/zanetworker/mcp-sse-client-python
- https://github.com/golf-mcp/golf

Additional tools may be added to addon/FreeCADMCP/sse_server/tools following the examples and these are automatically loaded into the server.

### Installation

On Ubuntu, copy the folder addon/FreeCADMCP to ~/snap/freecad/common/Mod/ and restart FreeCAD.

### Usage

In FreeCAD, select the workbench "MCP addon". 

Start the MCP server with the button labelled "Start RPC Server"

test*.py provide examples of tool invocation.