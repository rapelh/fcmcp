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

        print("\nInvoking tool 'App-DocumentObject-New'...")
        result = await client.invoke_tool(
            "App-DocumentObject-New", 
            {
                "Doc": "TestDoc",
                "Type": "Part::Box",
                "Name": "TestObj",
                "Properties":
                {
                    "Length": 20.0,
                    "Width": 20.0,
                    "Height": 20.0,
                }
            }
        )
        format_result(result)

        print("\nInvoking tool 'App-DocumentObject-Edit'...")
        result = await client.invoke_tool(
            "App-DocumentObject-Edit", 
            {
                "Doc": "TestDoc",
                "Name": "TestObj",
                "Properties":
                {
                    "Length": 30.0,
                    "Width": 40.0,
                    "Height": 50.0,
                }
            }
        )
        format_result(result)

        print("\nInvoking tool 'App-DocumentObject-Del'...")
        result = await client.invoke_tool(
            "App-DocumentObject-Del", 
            {
                "Doc": "TestDoc",
                "Name": "TestObj"
            }
        )
        format_result(result)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
    print("Script completed.")
