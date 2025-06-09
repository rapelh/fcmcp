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
                "DocName": "TestDoc"
            }
        )
        format_result(result)

        print("\nInvoking tool 'Draft-Arc-ByCenterRadiusAngles'...")
        result = await session.call_tool(
            "Draft-Arc-ByCenterRadiusAngles", 
            {
                "DocName": "TestDoc",
                "ObjLabel": "TestArcByCenterRadiusAngles",
                "Properties": {
                    "Center": {
                        "X": 10.0,
                        "Y": 20.0,
                        "Z": 30.0,
                    },
                    "Radius": 20.0,
                    "StartAngle": 40.0,
                    "EndAngle": 60.0,
                }
            }
        )
        format_result(result)

        print("\nInvoking tool 'Draft-Circle-ByCenterRadius'...")
        result = await session.call_tool(
            "Draft-Circle-ByCenterRadius", 
            {
                "DocName": "TestDoc",
                "ObjLabel": "TestCircle-ByCenterRadius",
                "Properties": {
                    "Center": {
                        "X": 10.0,
                        "Y": 20.0,
                        "Z": 30.0,
                    },
                    "Radius": 20.0,
                }
            }
        )
        format_result(result)

        print("\nInvoking tool 'Draft-Arc-ByThreeVectors'...")
        result = await session.call_tool(
            "Draft-Arc-ByThreeVectors", 
            {
                "DocName": "TestDoc",
                "ObjLabel": "TestArcByByThreeVectors",
                "Properties": {
                    "X1": 10.0,
                    "Y1": 20.0,
                    "Z1": 30.0,
                    "X2": 20.0,
                    "Y2": 10.0,
                    "Z2": 0.0,
                    "X3": 20.0,
                    "Y3": 20.0,
                    "Z3": 10.0,
                    "Radius": 20.0,
                    "StartAngle": 40.0,
                    "EndAngle": 60.0,
                }
            }
        )
        format_result(result)

        print("\nInvoking tool 'Part-RegularPolygon'...")
        result = await session.call_tool(
            "Part-RegularPolygon", 
            {
                "DocName": "TestDoc",
                "ObjName": "TestRegularPolygon",
                "Properties":
                {
                    "Polygon": 6,
                    "Circumradius": 200.0,
                }
            }
        )
        format_result(result)

        print("\nInvoking tool 'Draft-Fillet-FromTwoEdges'...")
        result = await session.call_tool(
            "Draft-Fillet-FromTwoEdges", 
            {
                "DocName": "TestDoc",
                "ObjName": "TestRegularPolygon",
                "Properties":
                {
                    "Label": "FilletFromTwoEdges",
                    "EdgeIndex1": 0,
                    "EdgeIndex2": 1,
                    "Radius": 10.0,
                }
            }
        )
        format_result(result)

        print("\nInvoking tool 'Draft-Fillet-FromObjectEdges'...")
        result = await session.call_tool(
            "Draft-Fillet-FromObjectEdges", 
            {
                "DocName": "TestDoc",
                "ObjName": "TestRegularPolygon",
                "Properties":
                {
                    "Label": "FilletFromObjectEdges",
                    #"ObjectEdgeIndices": [0, 1, 2],
                    "Radius": 10.0,
                }
            }
        )
        format_result(result)

        print("\nInvoking tool 'Draft-Circle-FromCircularEdge'...")
        result = await session.call_tool(
            "Draft-Circle-FromCircularEdge", 
            {
                "DocName": "TestDoc",
                "ObjLabel": "TestCircle-FromCircularEdge",
                "Properties": {
                    "EdgeObjectLabel": "FilletFromTwoEdges",
                    "EdgeIndex": 1,
                }
            }
        )
        format_result(result)

        print("\nInvoking tool 'Draft-Wire-FromVectors'...")
        result = await session.call_tool(
            "Draft-Wire-FromVectors", 
            {
                "DocName": "TestDoc",
                "ObjLabel": "TestWire-FromVectors",
                "Properties": {
                    "Vectors": [
                        [0.0, 10.0, 20.0],
                        [0.0, 5.0, 30.0],
                        [0.0, 15.0, 35.0],
                        [0.0, 20.0, 10.0],
                    ],
                    "Closed": True,
                    "Face": True,
                }
            }
        )
        format_result(result)

        print("\nInvoking tool 'Draft-BSpline-FromVectors'...")
        result = await session.call_tool(
            "Draft-BSpline-FromVectors", 
            {
                "DocName": "TestDoc",
                "ObjLabel": "TestBSpline-FromVectors",
                "Properties": {
                    "Vectors": [
                        [0.0, 10.0, 20.0],
                        [0.0, 5.0, 30.0],
                        [0.0, 15.0, 35.0],
                        [0.0, 20.0, 10.0],
                    ],
                    "Closed": False,
                    "Face": False,
                }
            }
        )
        format_result(result)



        print("\nInvoking tool 'Part-Wire'...")
        result = await session.call_tool(
            "Part-Wire", 
            {
                "DocName": "TestDoc",
                "ObjName": "TestWire",
                "Properties": {
                    "Vectors": [
                        [0.0, 30.0, 15.0],
                        [0.0, 55.0, 35.0],
                        [0.0, 15.0, 25.0],
                        [0.0, 25.0, 10.0],
                    ],
                }
            }
        )
        format_result(result)

        print("\nInvoking tool 'Draft-BSpline-FromWire'...")
        result = await session.call_tool(
            "Draft-BSpline-FromWire", 
            {
                "DocName": "TestDoc",
                "ObjLabel": "TestBSpline-FromWire",
                "Properties": {
                    "WireName": "TestWire",
                    "Closed": False,
                    "Face": False,
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
