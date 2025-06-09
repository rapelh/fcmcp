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

        print("\nInvoking tool 'Std-AxisCross'...")
        result = await session.call_tool(
            "Std-AxisCross", 
            {
                "Activate": True
            }
        )
        format_result(result)

        print("\nInvoking tool 'Std-GetCamera'...")
        result = await session.call_tool(
            "Std-GetCamera", 
            {}
        )
        format_result(result)

        print("\nInvoking tool 'Std-Open'...")
        result = await session.call_tool(
            "Std-Open", 
            {
                "Path": "/home/ralph-apel/snap/freecad/common/Mod/parts_library/Architectural Parts/Construction blocks/Canal block.FCStd"
            }
        )
        format_result(result)
                       
        print("\nInvoking tool 'Std-OrtographicCamera'...")
        result = await session.call_tool(
            "Std-OrtographicCamera", 
            {}
        )
        format_result(result)

        print("\nInvoking tool 'Std-PerspectiveCamera'...")
        result = await session.call_tool(
            "Std-PerspectiveCamera", 
            {}
        )
        format_result(result)
 
        print("\nInvoking tool 'Part-Box'...")
        result = await session.call_tool(
            "Part-Box", 
            {
                "DocName": "TestDoc",
                "ObjName": "TestBoxAAP",
                "Properties":
                {
                    "Length": 20.0,
                    "Width": 20.0,
                    "Height": 20.0,
                }
            }
        )
        format_result(result)

        print("\nInvoking tool 'Std-Placement' AAP ...")
        result = await session.call_tool(
            "Std-Placement", 
            {
                "DocName": "TestDoc",
                "ObjName": "TestBoxAAP",
                "Properties":
                {
                    "Position": {
                        "X": 120.0,
                        "Y": 80.0,
                        "Z": 100.0,                          
                    },
                    "Rotation": {
                        "Center": {
                            "X": 10.0,
                            "Y": 10.0,
                            "Z": 10.0,                          
                        },
                        "Angle": 20.0,
                        "Axis": {
                            "X": 0.0,
                            "Y": 0.0,
                            "Z": 1.0,                          
                        }
                    },
                }
            }
        )
        format_result(result)

        print("\nInvoking tool 'Part-Box'...")
        result = await session.call_tool(
            "Part-Box", 
            {
                "DocName": "TestDoc",
                "ObjName": "TestBoxPYPR",
                "Properties":
                {
                    "Length": 20.0,
                    "Width": 20.0,
                    "Height": 20.0,
                }
            }
        )
        format_result(result)

        print("\nInvoking tool 'Std-Placement' PYPR ...")
        result = await session.call_tool(
            "Std-Placement", 
            {
                "DocName": "TestDoc",
                "ObjName": "TestBoxPYPR",
                "Properties":
                {
                    "Position": {
                        "X": 220.0,
                        "Y": 180.0,
                        "Z": 200.0,                          
                    },
                    "Rotation": {
                        "Center": {
                            "X": 10.0,
                            "Y": 10.0,
                            "Z": 10.0,                          
                        },
                        "Yaw": 20.0,
                        "Pitch": 30.0,
                        "Roll": 45.0
                    },
                }
            }
        )
        format_result(result)

        print("\nInvoking tool 'Std-SetActiveDocument'...")
        result = await session.call_tool(
            "Std-SetActiveDocument", 
            {
                "DocName": "TestDoc"
            }
        )
        format_result(result)

        print("\nInvoking tool 'Std-SetStereoType'...")
        result = await session.call_tool(
            "Std-SetStereoType", 
            {
                "Type": "Anaglyph"
            }
        )
        format_result(result)

        print("\nInvoking tool 'Std-StoreWorkingView'...")
        result = await session.call_tool(
            "Std-StoreWorkingView", 
            {}
        )
        format_result(result)

        print("\nInvoking tool 'Std-RecallWorkingView'...")
        result = await session.call_tool(
            "Std-RecallWorkingView", 
            {}
        )
        format_result(result)

        print("\nInvoking tool 'Std-SaveAs'...")
        result = await session.call_tool(
            "Std-SaveAs", 
            {
                "DocName": "TestDoc",
                "Path": "/home/ralph-apel/TestDoc.FCStd"
            }
        )
        format_result(result)

        print("\nInvoking tool 'Std-ToggleSelectability'...")
        result = await session.call_tool(
            "Std-ToggleSelectability", 
            {
                "DocName": "TestDoc",
                "ObjName": "TestBoxAAP"
            }
        )
        format_result(result)

        print("\nInvoking tool 'Std-ToggleVisibility'...")
        result = await session.call_tool(
            "Std-ToggleVisibility", 
            {
                "DocName": "TestDoc",
                "ObjName": "TestBoxPYPR"
            }
        )
        format_result(result)

        print("\nInvoking tool 'Std-ViewBottom'...")
        result = await session.call_tool(
            "Std-ViewBottom", 
            {}
        )
        format_result(result)

        print("\nInvoking tool 'Std-ViewDimetric'...")
        result = await session.call_tool(
            "Std-ViewDimetric", 
            {}
        )
        format_result(result)

        print("\nInvoking tool 'Std-ViewFitAll'...")
        result = await session.call_tool(
            "Std-ViewFitAll", 
            {}
        )
        format_result(result)

        print("\nInvoking tool 'Std-ViewFitSelection'...")
        result = await session.call_tool(
            "Std-ViewFitSelection", 
            {}
        )
        format_result(result)

        print("\nInvoking tool 'Std-ViewFront'...")
        result = await session.call_tool(
            "Std-ViewFront", 
            {}
        )
        format_result(result)

        print("\nInvoking tool 'Std-ViewHome'...")
        result = await session.call_tool(
            "Std-ViewHome", 
            {}
        )
        format_result(result)

        print("\nInvoking tool 'Std-ViewIsometric'...")
        result = await session.call_tool(
            "Std-ViewIsometric", 
            {}
        )
        format_result(result)

        print("\nInvoking tool 'Std-ViewRear'...")
        result = await session.call_tool(
            "Std-ViewRear", 
            {}
        )
        format_result(result)

        print("\nInvoking tool 'Std-ViewRight'...")
        result = await session.call_tool(
            "Std-ViewRight", 
            {}
        )
        format_result(result)

        print("\nInvoking tool 'Std-ViewRotateLeft'...")
        result = await session.call_tool(
            "Std-ViewRotateLeft", 
            {}
        )
        format_result(result)

        print("\nInvoking tool 'Std-ViewRotateRight'...")
        result = await session.call_tool(
            "Std-ViewRotateRight", 
            {}
        )
        format_result(result)

        print("\nInvoking tool 'Std-ViewScreenshot'...")
        result = await session.call_tool(
            "Std-ViewScreenshot", 
            {
                "ViewName": "Isometric"
            }
        )
        format_result(result)

        print("\nInvoking tool 'Std-ViewTop'...")
        result = await session.call_tool(
            "Std-ViewTop", 
            {}
        )
        format_result(result)

        print("\nInvoking tool 'Std-ViewTrimetric'...")
        result = await session.call_tool(
            "Std-ViewTrimetric", 
            {}
        )
        format_result(result)

        print("\nInvoking tool 'Std-ViewZoomIn'...")
        result = await session.call_tool(
            "Std-ViewZoomIn", 
            {}
        )
        format_result(result)

        print("\nInvoking tool 'Std-ViewZoomOut'...")
        result = await session.call_tool(
            "Std-ViewZoomOut", 
            {}
        )
        format_result(result)

        print("\nInvoking tool 'Std-Workbench'...")
        result = await session.call_tool(
            "Std-Workbench", 
            {
                "Name": "Part"
            }
        )
        format_result(result)

        print("\nInvoking tool 'ExecuteCode'...")
        result = await session.call_tool(
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
        format_result(result)

        print("\nInvoking tool 'DumpDocument'...")
        result = await session.call_tool(
            "DumpDocument", 
            {
                "DocName": "TestDoc"
            }
        )
        format_result(result)

        print("\nInvoking tool 'Std-VarSet'...")
        result = await session.call_tool(
            "Std-VarSet", 
            {
                "DocName": "TestDoc",
                "ObjName": "TestVarSet",
                "Properties": {
                    "Variables": [
                        {
                            "Type": "App::PropertyInteger",
                            "Name": "I",
                            "Value": 1,
                        },
                        {
                            "Type": "App::PropertyBool",
                            "Name": "B",
                            "Value": True,
                        },
                        {
                            "Type": "App::PropertyString",
                            "Name": "S",
                            "Value": "blah",
                        },
                        {
                            "Type": "App::PropertyFloat",
                            "Name": "F",
                            "Value": 2.2,
                        }
                    ]
                }
            }
        )
        format_result(result)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
