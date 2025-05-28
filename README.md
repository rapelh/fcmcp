# fcmcp
==== MCP for FreeCAD 1.0+ ====

A MCP server as addon for FreeCAD 1.0+ with SSE transport, based on https://github.com/modelcontextprotocol/python-sdk.

Additional tools may be added to addon/FreeCADMCP/sse_server/tools following the examples and these are automatically loaded into the server.

== Installation ==

Copy the folder addon/FreeCADMCP to ~/snap/freecad/common/Mod/ and restart FreeCAD.

== Usage ==

In FreeCAD, select the workbenck "MCP addon". 

Start the MCP server with the button labelled "Start SSE Server"

sse_client.py provides examples of tool invokation.