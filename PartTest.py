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

        print("\nInvoking tool 'Part-Circle'...")
        result = await session.call_tool(
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
        format_result(result)

        print("\nInvoking tool 'Part-Cone'...")
        result = await session.call_tool(
            "Part-Cone", 
            {
                "Doc": "TestDoc",
                "Name": "TestCone",
                "Properties":
                {
                    "Radius1": 30.0,
                    "Radius2": 80.0,
                    "Height": 100.0,
                    "Angle": 150.0,
                }
            }
        )
        format_result(result)

        print("\nInvoking tool 'Part-Cylinder'...")
        result = await session.call_tool(
            "Part-Cylinder", 
            {
                "Doc": "TestDoc",
                "Name": "TestCylinder",
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
        format_result(result)

        print("\nInvoking tool 'Part-Ellipse'...")
        result = await session.call_tool(
            "Part-Ellipse", 
            {
                "Doc": "TestDoc",
                "Name": "TestEllipse",
                "Properties":
                {
                    "MajorRadius": 130.0,
                    "MinorRadius": 80.0,
                    "Angle1": 50.0,
                    "Angle2": 125.0,
                }
            }
        )
        format_result(result)

        print("\nInvoking tool 'Part-Ellipsoid'...")
        result = await session.call_tool(
            "Part-Ellipsoid", 
            {
                "Doc": "TestDoc",
                "Name": "TestEllipsoid",
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
        format_result(result)

        print("\nInvoking tool 'Part-Helix'...")
        result = await session.call_tool(
            "Part-Helix", 
            {
                "Doc": "TestDoc",
                "Name": "TestHelix",
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
        format_result(result)

        print("\nInvoking tool 'Part-Line'...")
        result = await session.call_tool(
            "Part-Line", 
            {
                "Doc": "TestDoc",
                "Name": "TestLine",
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
        format_result(result)

        print("\nInvoking tool 'Part-Plane'...")
        result = await session.call_tool(
            "Part-Plane", 
            {
                "Doc": "TestDoc",
                "Name": "TestPlane",
                "Properties":
                {
                    "Length": 180.0,
                    "Width": 325.0,
                }
            }
        )
        format_result(result)

        print("\nInvoking tool 'Part-Point'...")
        result = await session.call_tool(
            "Part-Point", 
            {
                "Doc": "TestDoc",
                "Name": "TestPoint",
                "Properties":
                {
                    "X": 180.0,
                    "Y": 325.0,
                    "Z": 225.0,
                }
            }
        )
        format_result(result)

        print("\nInvoking tool 'Part-Prism'...")
        result = await session.call_tool(
            "Part-Prism", 
            {
                "Doc": "TestDoc",
                "Name": "TestPrism",
                "Properties":
                {
                    "Polygon": 5,
                    "Circumradius": 125.0,
                    "Height": 225.0,
                    "Height": 225.0,
                }
            }
        )
        format_result(result)

        print("\nInvoking tool 'Part-RegularPolygon'...")
        result = await session.call_tool(
            "Part-RegularPolygon", 
            {
                "Doc": "TestDoc",
                "Name": "TestRegularPolygon",
                "Properties":
                {
                    "Polygon": 6,
                    "Circumradius": 225.0,
                }
            }
        )
        format_result(result)

        print("\nInvoking tool 'Part-Sphere'...")
        result = await session.call_tool(
            "Part-Sphere", 
            {
                "Doc": "TestDoc",
                "Name": "TestSphere",
                "Properties":
                {
                    "Radius": 60.0,
                    "Angle1": -25.0,
                    "Angle2": 25.0,
                    "Angle3": 55.0,
                }
            }
        )
        format_result(result)

        print("\nInvoking tool 'Part-Spiral'...")
        result = await session.call_tool(
            "Part-Spiral", 
            {
                "Doc": "TestDoc",
                "Name": "TestSpiral",
                "Properties":
                {
                    "Radius": 160.0,
                    "Growth": 5.0,
                    "Rotations": 5,
                    "SegmentLength": 1,
                }
            }
        )
        format_result(result)

        print("\nInvoking tool 'Part-Torus'...")
        result = await session.call_tool(
            "Part-Torus", 
            {
                "Doc": "TestDoc",
                "Name": "TestTorus",
                "Properties":
                {
                    "Radius1": 160.0,
                    "Radius2": 20.0,
                    "Angle1": 50.0,
                    "Angle2": -30.0,
                    "Angle3": 180.0,
                }
            }
        )
        format_result(result)

        print("\nInvoking tool 'Part-Tube'...")
        result = await session.call_tool(
            "Part-Tube", 
            {
                "Doc": "TestDoc",
                "Name": "TestTube",
                "Properties":
                {
                    "InnerRadius": 40.0,
                    "OuterRadius": 60.0,
                    "Height": 150.0,
                }
            }
        )
        format_result(result)

        print("\nInvoking tool 'Part-Wedge'...")
        result = await session.call_tool(
            "Part-Wedge", 
            {
                "Doc": "TestDoc",
                "Name": "TestWedge",
                "Properties":
                {
                    "Xmin": 0.0,
                    "Ymin": 0.0,
                    "Zmin": 0.0,
                    "X2min": 2.0,
                    "Z2min": 2.0,
                    "Xmax": 10.0,
                    "Ymax": 10.0,
                    "Zmax": 10.0,
                    "X2max": 8.0,
                    "Z2max": 8.0,
                }
            }
        )
        format_result(result)

        print("\nInvoking tool 'Part-Extrusion'...")
        result = await session.call_tool(
            "Part-Extrusion", 
            {
                "Doc": "TestDoc",
                "Name": "TestExtrude",
                "Properties":
                {
                    "Base": "TestCircle",
                    "DirMode": "Custom",
                    "Dir": {
                        "X": 0.0,
                        "Y": 0.0,
                        "Z": 1.0,
                    },
                    "DirLink": "",
                    "LengthFwd": 20.0,
                    "LengthRev": 10.0,
                    "Solid": False,
                    "Reversed": False,
                    "Symmetric": False,
                    "TaperAngle": 0.0,
                    "TaperAngleRev": 0.0,
                }
            }
        )
        format_result(result)

        print("\nInvoking tool 'DumpDocument'...")
        result = await session.call_tool(
            "DumpDocument", 
            {
                "Doc": "TestDoc",
                "Properties":
                {}
            }
        )
        format_result(result)

        print("\nInvoking tool 'Part-LineSegment'...")
        result = await session.call_tool(
            "Part-LineSegment", 
            {
                "Doc": "TestDoc",
                "Name": "TestLineSegment",
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