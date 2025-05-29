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
        
        print("\nInvoking tool 'App-Version'...")
        result = await client.invoke_tool(
            "App-Version", 
            {}
        )
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")

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
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")

        print("\nInvoking tool 'App-DocumentObject-New'...")
        result = await client.invoke_tool(
            "App-DocumentObject-New", 
            {
                "Doc": "TestDoc",
                "Type": "Part::Cylinder",
                "Name": "MidObj",
                "Properties":
                {
                    "Radius": 20.0,
                    "Height": 20.0,
                }
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
                "Type": "Part::Sphere",
                "Name": "ThirdObj",
                "Properties":
                {
                    "Radius": 20.0,
                }
            }
        )
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")

        print("\nInvoking tool 'App-DocumentObject-Del'...")
        result = await client.invoke_tool(
            "App-DocumentObject-Del", 
            {
                "Doc": "TestDoc",
                "Name": "MidObj"
            }
        )
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")

        print("\nInvoking tool 'ExecuteCode'...")
        result = await client.invoke_tool(
            "ExecuteCode", 
            {
                "Code": '''
import FreeCAD as App
doc = App.getDocument("TestDoc")
prism = doc.addObject("Part::Prism", "myPrism")
prism.Polygon = 5\nprism.Circumradius = 10
prism.Height = 50\nprism.FirstAngle = 22.5
prism.SecondAngle = 45
prism.Placement = App.Placement(App.Vector(1, 2, 3), App.Rotation(60, 75, 30))
doc.recompute()
'''
            }
        )
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")

        # print("\nInvoking tool 'Std-MergeProject-FromPartsLibrary'...")
        # result = await client.invoke_tool(
        #     "Std-MergeProject-FromPartsLibrary", 
        #     {
        #         "RelativePath": "Architectural Parts/Construction blocks/Canal block.FCStd"
        #     }
        # )
        # print(f"\nTool result: {result.content}")
        # print(f"Error code: {result.error_code}")
        # result_dict = json.loads(result.content)
        # print(f"Dict: {result_dict}")

        # print("\nInvoking tool 'Std-ViewScreenshot'...")
        # result = await client.invoke_tool(
        #     "Std-ViewScreenshot", 
        #     {
        #         "ViewName": "Isometric"
        #     }
        # )
        # print(f"\nTool result: {result.content}")
        # print(f"Error code: {result.error_code}")
        # result_dict = json.loads(result.content)
        # print(f"Dict: {result_dict}")

        # png_data = base64.b64decode(result_dict['data'])
        # with open('test.png', 'wb') as f:
        #     f.write(png_data)

        # print("\nInvoking tool 'list_document'...")
        # result = await client.invoke_tool(
        #     "list_document", 
        #     {
        #         "name": "TestDoc"
        #     }
        # )
        # print(f"\nTool result: {result.content}")
        # print(f"Error code: {result.error_code}")

        print("\nInvoking tool 'Std-Open'...")
        result = await client.invoke_tool(
            "Std-Open", 
            {
                "Path": "/home/ralph-apel/snap/freecad/common/Mod/parts_library/Architectural Parts/Construction blocks/Canal block.FCStd"
            }
        )
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")

        # print("\nInvoking tool 'Std-SaveAs'...")
        # result = await client.invoke_tool(
        #     "Std-SaveAs", 
        #     {
        #         "Doc": "TestDoc",
        #         "Path": "./TestDoc.FCStd"
        #     }
        # )
        # print(f"\nTool result: {result.content}")
        # print(f"Error code: {result.error_code}")
        # result_dict = json.loads(result.content)
        # print(f"Dict: {result_dict}")

        # print("\nInvoking tool 'Std-ToggleVisibility'...")
        # result = await client.invoke_tool(
        #     "Std-ToggleVisibility", 
        #     {
        #         "Doc": "TestDoc",
        #         "Name": "ThirdObj"
        #     }
        # )
        # print(f"\nTool result: {result.content}")
        # print(f"Error code: {result.error_code}")
        # result_dict = json.loads(result.content)
        # print(f"Dict: {result_dict}")

        print("\nInvoking tool 'Part-Box'...")
        result = await client.invoke_tool(
            "Part-Box", 
            {
                "Doc": "TestDoc",
                "Name": "PartBox",
                "Properties": {
                    "Length": 135,
                    "Width": 155,
                    "Height": 185
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
                "Name": "PartCylinder",
                "Properties": {
                    "Radius": 35,
                    "Height": 185
                }
            }
        )
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")

        print("\nInvoking tool 'Part-Sphere'...")
        result = await client.invoke_tool(
            "Part-Sphere", 
            {
                "Doc": "TestDoc",
                "Name": "PartSphere",
                "Properties": {
                    "Radius": 75,
                }
            }
        )
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")

        print("\nInvoking tool 'Std-SetActiveDocument'...")
        result = await client.invoke_tool(
            "Std-SetActiveDocument", 
            {
                "Doc": "Canal_block",
                "Properties": { }
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
