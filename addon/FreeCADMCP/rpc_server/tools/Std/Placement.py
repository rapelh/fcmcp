import mcp.types as types
import FreeCAD
import json
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue
from rpc_server.serialize import serialize_object

tool_type = types.Tool(
                name="Std-Placement",
                description="Set position  a and rotation ofnamed object in a named document",
                inputSchema={
                    "type": "object",
                    "required": ["Doc", "Name", "Mode"],
                    "properties": {
                        "Doc": {
                            "type": "string",
                            "description": "Name of document in which to create",
                        },
                        "Name": {
                            "type": "string",
                            "description": "Name of object to create",
                        },
                        "Position": {
                            "X": {
                                "type": "number",
                                "description": "X for Position",
                            },
                            "Y": {
                                "type": "number",
                                "description": "Y for Position",
                            },
                            "Z": {
                                "type": "number",
                                "description": "Z for Position",
                            },
                        },
                        "Rotation": {
                            "Mode": {
                                "type": "string",
                                "description": "AAP (angle, axis, position) or PYPR (position, yaw, pitch, roll)",
                            },
                            "Center": {
                                "X": {
                                    "type": "number",
                                    "description": "X for Center",
                                },
                                "Y": {
                                    "type": "number",
                                    "description": "Y for Center",
                                },
                                "Z": {
                                    "type": "number",
                                    "description": "Z for Center",
                                },
                            },
                            "Angle": {
                                "type": "number",
                                "description": "Angle for AAP",
                            },
                            "Axis": {
                                "X": {
                                    "type": "number",
                                    "description": "X for Axis",
                                },
                                "Y": {
                                    "type": "number",
                                    "description": "Y for Axis",
                                },
                                "Z": {
                                    "type": "number",
                                    "description": "Z for Axis",
                                },
                            },
                            "Yaw": {
                                "type": "number",
                                "description": "Yaw for PYPR",
                            },
                            "Pitch": {
                                "type": "number",
                                "description": "Pitch for PYPR",
                            },
                            "Roll": {
                                "type": "number",
                                "description": "Roll for PYPR",
                            },
                        },
                    },
                },
            )

def do_it(args):
    doc_name = args.get("Doc")
    obj_name = args.get("Name")
    position = args.get("Position", {"X": 0, "Y": 0, "Z": 0})
    rotation = args.get("Rotation")
    mode = rotation.get("Mode")
    center = rotation.get("Center", {"X": 0, "Y": 0, "Z": 0})
    if mode == "AAP":
        angle = rotation.get("Angle", 0)
        axis = rotation.get("Axis", {"X": 0, "Y": 0, "Z": 1})
        rpc_request_queue.put(lambda: _aap_placement_gui(doc_name, obj_name, angle, axis, position, center))
        res, text = rpc_response_queue.get()
        if res is True:
            return [types.TextContent(type="text", text=text)]
        else:
            return [types.TextContent(type="text", text=text)]
    elif mode == "PYPR":
        yaw = rotation.get("Yaw", 0)
        pitch = rotation.get("Pitch", 0)
        roll = rotation.get("Roll", 0)
        rpc_request_queue.put(lambda: _pypr_placement_gui(doc_name, obj_name, position, yaw, pitch, roll, center))
        res, text = rpc_response_queue.get()
        if res is True:
            return [types.TextContent(type="text", text=text)]
        else:
            return [types.TextContent(type="text", text=text)]
    else:
            return [types.TextContent(type="text", text=f"Unknown rotation mode {mode}")]

def _aap_placement_gui(doc_name: str, obj_name: str, angle: float, axis: dict[str, float], position: dict[str, float], center: dict[str, float]):
    doc = FreeCAD.getDocument(doc_name)
    if not doc:
        FreeCAD.Console.PrintError(f"Document '{doc_name}' not found.\n")
        return f"Document '{doc_name}' not found.\n"
    obj = doc.getObject(obj_name)
    if not obj:
        FreeCAD.Console.PrintError(f"Object '{obj_name}' not found in document '{doc_name}'.\n")
        return f"Object '{obj_name}' not found in document '{doc_name}'.\n"
    try:
        pos = FreeCAD.Vector(position["X"], position["Y"], position["Z"])
        rot = FreeCAD.Rotation(FreeCAD.Vector(axis["X"], axis["Y"], axis["Z"]), angle)
        ctr = FreeCAD.Vector(center["X"], center["Y"], center["Z"])
        plc = FreeCAD.Placement(pos, rot, ctr)
        obj.Placement = plc
        return True, json.dumps(serialize_object(obj))
    except Exception as e:
        return False, str(e)

def _pypr_placement_gui(doc_name: str, obj_name: str, position: dict[str, float], yaw: float, pitch: float, roll: float, center: dict[str, float]):
    doc = FreeCAD.getDocument(doc_name)
    if not doc:
        FreeCAD.Console.PrintError(f"Document '{doc_name}' not found.\n")
        return f"Document '{doc_name}' not found.\n"
    obj = doc.getObject(obj_name)
    if not obj:
        FreeCAD.Console.PrintError(f"Object '{obj_name}' not found in document '{doc_name}'.\n")
        return f"Object '{obj_name}' not found in document '{doc_name}'.\n"
    try:
        pos = FreeCAD.Vector(position["X"], position["Y"], position["Z"])
        rot = FreeCAD.Rotation(yaw, pitch, roll)
        ctr = FreeCAD.Vector(center["X"], center["Y"], center["Z"])
        plc = FreeCAD.Placement(pos, rot, ctr)
        obj.Placement = plc
        return True, json.dumps(serialize_object(obj))
    except Exception as e:
        return False, str(e)