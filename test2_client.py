"""
MCP SSE Client Usage Example

This script demonstrates how to use the MCPClient to interact with an MCP endpoint,
list available tools, and invoke a tool with parameters.
"""

import asyncio
import base64
import json
import sys
from client.mcp_sse_client.client import MCPClient

async def main():
    print("Starting MCPClient example...")
    try:
        # Initialize the client
        print("Initializing client...")
        client = MCPClient("http://localhost:9875/sse")
        
        # List available tools
        print("Listing available tools...")
        tools = await client.list_tools()
        print("Available tools:")
        for tool in tools:
            print(f"- {tool.name}: {tool.description}")
            print("  Parameters:")
            for param in tool.parameters:
                print(f"    - {param.name} ({param.parameter_type}): {param.description}")

        print("\nInvoking tool 'Std-New'...")
        result = await client.invoke_tool(
            "Std-New", 
            {
                "Name": "TestDoc"
            }
        )
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")

        print("\nInvoking tool 'App-DocumentObject-New'...")
        result = await client.invoke_tool(
            "App-DocumentObject-New", 
            {
                "Doc": "TestDoc",
                "Type": "Part::Box",
                "Name": "TestObj",
                "Properties":
                {
                    "Length": 10.0,
                    "Width": 20.0,
                    "Height": 30.0,
                }
            }
        )
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")


        print("\nInvoking tool 'Std-ViewIsometric'...")
        result = await client.invoke_tool(
            "Std-ViewIsometric", 
            {}
        )
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")

        print("\nInvoking tool 'Std-ViewFitAll'...")
        result = await client.invoke_tool(
            "Std-ViewFitAll", 
            {}
        )
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")

        print("\nInvoking tool 'Std-Placement' in mode AAP ...")
        result = await client.invoke_tool(
            "Std-Placement", 
            {
                "Doc": "TestDoc",
                "Name": "TestObj",
                "Position": {
                    "X": 90.0,
                    "Y": 120.0,
                    "Z": 150.0
                },
                "Rotation": {
                    "Mode": "AAP",
                    "Center": {
                        "X": 10,
                        "Y": 10,
                        "Z": 0
                    },
                    "Angle": 45.0,
                    "Axis": {
                        "X": 0,
                        "Y": 0,
                        "Z": 1
                    }
                }
            }
        )
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")

        print("\nInvoking tool 'Std-ViewFitAll'...")
        result = await client.invoke_tool(
            "Std-ViewFitAll", 
            {}
        )
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")

        print("\nInvoking tool 'App-DocumentObject-New'...")
        result = await client.invoke_tool(
            "App-DocumentObject-New", 
            {
                "Doc": "TestDoc",
                "Type": "Part::Box",
                "Name": "TestObj2",
                "Properties":
                {
                    "Length": 100.0,
                    "Width": 50.0,
                    "Height": 5.0,
                }
            }
        )
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")

        print("\nInvoking tool 'Std-ViewFitAll'...")
        result = await client.invoke_tool(
            "Std-ViewFitAll", 
            {}
        )
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")

        print("\nInvoking tool 'Std-Placement' in mode AAP ...")
        result = await client.invoke_tool(
            "Std-Placement", 
            {
                "Doc": "TestDoc",
                "Name": "TestObj2",
                "Position": {
                    "X": 90.0,
                    "Y": 120.0,
                    "Z": 150.0
                },
                "Rotation": {
                    "Mode": "PYPR",
                    "Center": {
                        "X": 50,
                        "Y": 25,
                        "Z": 0
                    },
                    "Yaw": 45.0,
                    "Pitch": 10.0,
                    "Roll": 30.0
                }
            }
        )
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")

        print("\nInvoking tool 'Std-ViewFitAll'...")
        result = await client.invoke_tool(
            "Std-ViewFitAll", 
            {}
        )
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")

        print("\nInvoking tool 'Std-ToggleVisibility'...")
        result = await client.invoke_tool(
            "Std-ToggleVisibility", 
            {
                "Doc": "TestDoc",
                "Name": "TestObj"
            }
        )
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")

        print("\nInvoking tool 'Std-ViewFitAll'...")
        result = await client.invoke_tool(
            "Std-ViewFitAll", 
            {}
        )
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
    print("Script completed.")
