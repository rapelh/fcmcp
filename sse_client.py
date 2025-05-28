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
        
        print("\nInvoking tool 'app-version'...")
        result = await client.invoke_tool(
            "app-version", 
            {}
        )
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")

        print("\nInvoking tool 'std-new'...")
        result = await client.invoke_tool(
            "std-new", 
            {
                "Name": "TestDoc"
            }
        )
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")

        print("\nInvoking tool 'app-documentobject-new'...")
        result = await client.invoke_tool(
            "app-documentobject-new", 
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

        print("\nInvoking tool 'app-documentobject-edit'...")
        result = await client.invoke_tool(
            "app-documentobject-edit", 
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

        print("\nInvoking tool 'app-documentobject-new'...")
        result = await client.invoke_tool(
            "app-documentobject-new", 
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

        print("\nInvoking tool 'app-documentobject-new'...")
        result = await client.invoke_tool(
            "app-documentobject-new", 
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

        print("\nInvoking tool 'app-documentobject-del'...")
        result = await client.invoke_tool(
            "app-documentobject-del", 
            {
                "Doc": "TestDoc",
                "Name": "MidObj"
            }
        )
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")

        print("\nInvoking tool 'executecode'...")
        result = await client.invoke_tool(
            "executecode", 
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

        print("\nInvoking tool 'std-mergeproject-frompartslibrary'...")
        result = await client.invoke_tool(
            "std-mergeproject-frompartslibrary", 
            {
                "RelativePath": "Architectural Parts/Construction blocks/Canal block.FCStd"
            }
        )
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")

        print("\nInvoking tool 'std-viewscreenshot'...")
        result = await client.invoke_tool(
            "std-viewscreenshot", 
            {
                "ViewName": "Isometric"
            }
        )
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")

        png_data = base64.b64decode(result_dict['data'])
        with open('test.png', 'wb') as f:
            f.write(png_data)

        # print("\nInvoking tool 'list_document'...")
        # result = await client.invoke_tool(
        #     "list_document", 
        #     {
        #         "name": "TestDoc"
        #     }
        # )
        # print(f"\nTool result: {result.content}")
        # print(f"Error code: {result.error_code}")

        print("\nInvoking tool 'std-open'...")
        result = await client.invoke_tool(
            "std-open", 
            {
                "Path": "/home/ralph-apel/snap/freecad/common/Mod/parts_library/Architectural Parts/Construction blocks/Canal block.FCStd"
            }
        )
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")

        print("\nInvoking tool 'std-saveas'...")
        result = await client.invoke_tool(
            "std-saveas", 
            {
                "Doc": "TestDoc",
                "Path": "./TestDoc.FCStd"
            }
        )
        print(f"\nTool result: {result.content}")
        print(f"Error code: {result.error_code}")
        result_dict = json.loads(result.content)
        print(f"Dict: {result_dict}")

        print("\nInvoking tool 'std-togglevisibility'...")
        result = await client.invoke_tool(
            "std-togglevisibility", 
            {
                "Doc": "TestDoc",
                "Name": "ThirdObj"
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
