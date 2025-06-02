"""
MCP SSE Client Usage Example

This script demonstrates how to use the MCPClient to interact with an MCP endpoint,
list available tools, and invoke a tool with parameters.
"""

import asyncio
import json
import sys
from client.mcp_sse_client.client import MCPClient

def format_result(result):
    res_dict = json.loads(result.content)
    if result.error_code == 0:
        print("Success")
        if res_dict["type"] == "text":
            print(res_dict["text"])
        elif res_dict["type"] == "image":
            print(res_dict["data"], res_dict["mimeType"])
    else:
        print("Failure", result.error_code)
        if res_dict["type"] == "text":
            print(res_dict["text"])

async def main():
    print("Starting MCPClient ...")
    try:
        # Initialize the client
        print("Initializing client...")
        client = MCPClient("http://localhost:9875/sse")

        print("\nInvoking tool 'Std-New'...")
        result = await client.invoke_tool(
            "Std-New", 
            {
                "Name": "TestDoc"
            }
        )
        format_result(result)

        print("\nInvoking tool 'Draft-Line-FromVectors'...")
        result = await client.invoke_tool(
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
        result = await client.invoke_tool(
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
        result = await client.invoke_tool(
            "Draft-Wire-FromVectors", 
            {
                "Doc": "TestDoc",
                "Label": "TestWireFromVectors",
                "Properties":
                {
                    "Vectors": [[15.0, 25.0, 35.0], [15.0, 45.0, 65.0]]
                }
            }
        )
        format_result(result)

        print("\nInvoking tool 'Std-ViewFitAll'...")
        result = await client.invoke_tool(
            "Std-ViewFitAll", 
            {}
        )
        format_result(result)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
    print("Script completed.")
