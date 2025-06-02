"""
MCP Streamable Http Client Usage Example

This script demonstrates how to use the MCPClient to interact with an MCP endpoint,
list available tools, and invoke a tool with parameters.
"""

import asyncio
import json
import sys
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession

def format_result(result):
    print('format_result result', result)
    # meta=None content=[TextContent(type='text', text='TestDoc created', annotations=None)] isError=False
    content = result.content
    if not result.isError :
        print("Success")
        for cont in content:
            if cont.type == "text":
                print(cont.text)
            elif cont.type == "image":
                print(cont.data, cont.mimeType)
    else:
        print("Failure")
        for cont in content:
            if cont.type == "text":
                print(cont.text)

async def call_tools(session):
    try:
        # List available tools
        print("Listing available tools...")
        messages = await session.list_tools()
        print("Available tools:")
        for msg in messages:
            if msg[0] == 'tools':
                for tool in msg[1]:
                    print(f"- {tool}")
            #print("  Parameters:")
            #for param in tool.parameters:
            #    print(f"    - {param.name} ({param.parameter_type}): {param.description}")

        print("\nInvoking tool 'Std-New'...")
        result = await session.call_tool(
            "Std-New", 
            {
                "Name": "TestDoc"
            }
        )
        format_result(result)

        print("\nInvoking tool 'Draft-Line-FromVectors'...")
        result = await session.call_tool(
            "Draft-Line-FromVectors", 
            {
                "Doc": "TestDoc",
                "Label": "TestLineFromVectors_1",
                "Properties":
                {
                    "X1": 10.0,
                    "Y1": 20.0,
                    "Z1": 30.0,
                    "X2": 20.0,
                    "Y2": 40.0,
                    "Z2": 60.0,
                }
            }
        )
        format_result(result)

        print("\nInvoking tool 'Draft-Line-FromVectors'...")
        result = await session.call_tool(
            "Draft-Line-FromVectors", 
            {
                "Doc": "TestDoc",
                "Label": "TestLineFromVectors_2",
                "Properties":
                {
                    "X1": 15.0,
                    "Y1": 25.0,
                    "Z1": 35.0,
                    "X2": 25.0,
                    "Y2": 45.0,
                    "Z2": 65.0,
                }
            }
        )
        format_result(result)

        print("\nInvoking tool 'Draft-Wire-FromVectors'...")
        result = await session.call_tool(
            "Draft-Wire-FromVectors", 
            {
                "Doc": "TestDoc",
                "Label": "TestWireFromVectors_2",
                "Properties":
                {
                    "Vectors": [[15.0, 25.0, 35.0], [15.0, 45.0, 65.0]],
                    "Closed": True,
                    "Face": False
                }
            }
        )
        format_result(result)

        print("\nInvoking tool 'Std-ViewFitAll'...")
        result = await session.call_tool(
            "Std-ViewFitAll", 
            {}
        )
        format_result(result)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()

async def main():
    print("Starting MCPClient ...")

    # Connect to a streamable HTTP server
    async with streamablehttp_client("http://localhost:9875/mcp") as (
        read_stream,
        write_stream,
        _,
    ):
        # Create a session using the client streams
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()
            # Call tools
            tasks = asyncio.gather(call_tools(session))
            await tasks

if __name__ == "__main__":
    asyncio.run(main())
    print("Script completed.")
