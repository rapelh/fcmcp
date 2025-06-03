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
                "Label": "TestWireFromVectors",
                "Properties":
                {
                    "Vectors": [[15.0, 25.0, 35.0], [15.0, 45.0, 65.0]],
                    "Closed": True,
                    "Face": False
                }
            }
        )
        format_result(result)

        print("\nInvoking tool 'Part-Box'...")
        result = await session.call_tool(
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
