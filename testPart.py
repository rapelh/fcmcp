"""
MCP SSE Client Usage Example

This script demonstrates how to use the MCPClient to interact with an MCP endpoint,
list available tools, and invoke a tool with parameters.
"""

import asyncio
import json
import sys
from client.mcp_sse_client.client import MCPClient

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
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")

        print("\nInvoking tool 'Part-Box..")
        result = await client.invoke_tool(
            "Part-Box", 
            {
                "Doc": "TestDoc",
                "Name": "TestBox",
                "Properties":
                {
                    "Length": 20.0,
                    "Width": 20.0,
                    "Height": 20.0,
                }
            }
        )
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")

        print("\nInvoking tool 'Part-Circle'...")
        result = await client.invoke_tool(
            "Part-Circle", 
            {
                "Doc": "TestDoc",
                "Name": "TestCircle",
                "Properties":
                {
                    "Radius": 30.0,
                    "Angle1": 40.0,
                    "Angle2": 150.0,
                }
            }
        )
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")

        print("\nInvoking tool 'Part-Cone'...")
        result = await client.invoke_tool(
            "Part-Cone", 
            {
                "Doc": "TestDoc",
                "Name": "TestCone"
                "Properties":
                {
                    "Radius1": 30.0,
                    "Radius2": 80.0,
                    "Height": 100.0,
                    "Angle": 150.0,
                }
            }
        )
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")

        print("\nInvoking tool 'Part-Cylinder'...")
        result = await client.invoke_tool(
            "Part-Cylinder", 
            {
                "Doc": "TestDoc",
                "Name": "TestCylinder"
                "Properties":
                {
                    "Radius": 30.0,
                    "Height": 100.0,
                    "Angle": 250.0,
                    "FirstAngle": 25.0,
                    "SecondAngle": 10.0,
                }
            }
        )
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")

        print("\nInvoking tool 'Part-Ellipse'...")
        result = await client.invoke_tool(
            "Part-Ellipse", 
            {
                "Doc": "TestDoc",
                "Name": "TestEllipse"
                "Properties":
                {
                    "MajorRadius": 130.0,
                    "MinorRadius": 80.0,
                    "Angle1": 50.0,
                    "Angle2": 125.0,
                }
            }
        )
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")

        print("\nInvoking tool 'Part-Ellipsoid'...")
        result = await client.invoke_tool(
            "Part-Ellipsoid", 
            {
                "Doc": "TestDoc",
                "Name": "TestEllipsoid"
                "Properties":
                {
                    "Radius1": 130.0,
                    "Radius2": 80.0,
                    "Radius3": 40.0,
                    "Angle1": 50.0,
                    "Angle2": 125.0,
                    "Angle3": 155.0,
                }
            }
        )
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")

        print("\nInvoking tool 'Part-Helix'...")
        result = await client.invoke_tool(
            "Part-Helix", 
            {
                "Doc": "TestDoc",
                "Name": "TestHelix"
                "Properties":
                {
                    "Pitch": 10.0,
                    "Height": 180.0,
                    "Radius": 40.0,
                    "SegmentLength": 50.0,
                    "Angle": 25.0,
                }
            }
        )
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")

        print("\nInvoking tool 'Part-Line'...")
        result = await client.invoke_tool(
            "Part-Line", 
            {
                "Doc": "TestDoc",
                "Name": "TestLine"
                "Properties":
                {
                    "X1": 10.0,
                    "Y1": 180.0,
                    "Z1": 40.0,
                    "X2": 50.0,
                    "Y2": 25.0,
                    "Z2": 325.0,
                }
            }
        )
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")

        print("\nInvoking tool 'Part-Plane'...")
        result = await client.invoke_tool(
            "Part-Plane", 
            {
                "Doc": "TestDoc",
                "Name": "TestPlane"
                "Properties":
                {
                    "Length": 180.0,
                    "Width": 325.0,
                }
            }
        )
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")

        print("\nInvoking tool 'Part-Point'...")
        result = await client.invoke_tool(
            "Part-Point", 
            {
                "Doc": "TestDoc",
                "Name": "TestPoint"
                "Properties":
                {
                    "X": 180.0,
                    "Y": 325.0,
                    "Z": 225.0,
                }
            }
        )
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")

        print("\nInvoking tool 'Part-Prism'...")
        result = await client.invoke_tool(
            "Part-Prism", 
            {
                "Doc": "TestDoc",
                "Name": "TestPrism"
                "Properties":
                {
                    "Polygon": 5,
                    "Circumradius": 125.0,
                    "Height": 225.0,
                    "Height": 225.0,
                }
            }
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
