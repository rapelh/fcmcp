import sys
from testClients import format_result

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

        print("\nInvoking tool 'Std-New'...")
        result = await session.call_tool(
            "Std-New", 
            {
                "Name": "TestDoc"
            }
        )
        format_result(result)

        print("\nInvoking tool 'App-DocumentObject-New'...")
        result = await session.call_tool(
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
        result = await session.call_tool(
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
        result = await session.call_tool(
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
