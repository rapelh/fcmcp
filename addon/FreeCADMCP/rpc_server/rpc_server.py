import FreeCAD
import FreeCADGui

import queue
import importlib
import os
import threading
from dataclasses import dataclass, field
from typing import Any
import mcp.types as types
from mcp.server.lowlevel import Server
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.responses import Response
from starlette.routing import Mount, Route
import uvicorn


from PySide import QtCore

#from .parts_library import get_parts_list, insert_part_from_library
#from .serialize import serialize_object

rpc_server_instance = None
rpc_server_thread = None

# GUI task queue
rpc_request_queue = queue.Queue()
rpc_response_queue = queue.Queue()

def process_gui_tasks():
    while not rpc_request_queue.empty():
        task = rpc_request_queue.get()
        res = task()
        if res is not None:
            rpc_response_queue.put(res)
    QtCore.QTimer.singleShot(500, process_gui_tasks)


@dataclass
class Object:
    name: str
    type: str | None = None
    analysis: str | None = None
    properties: dict[str, Any] = field(default_factory=dict)


def set_object_property(
    doc: FreeCAD.Document, obj: FreeCAD.DocumentObject, properties: dict[str, Any]
):
    for prop, val in properties.items():
        try:
            if prop in obj.PropertiesList:
                if prop == "Placement" and isinstance(val, dict):
                    if "Base" in val:
                        pos = val["Base"]
                    elif "Position" in val:
                        pos = val["Position"]
                    else:
                        pos = {}
                    rot = val.get("Rotation", {})
                    placement = FreeCAD.Placement(
                        FreeCAD.Vector(
                            pos.get("x", 0),
                            pos.get("y", 0),
                            pos.get("z", 0),
                        ),
                        FreeCAD.Rotation(
                            FreeCAD.Vector(
                                rot.get("Axis", {}).get("x", 0),
                                rot.get("Axis", {}).get("y", 0),
                                rot.get("Axis", {}).get("z", 1),
                            ),
                            rot.get("Angle", 0),
                        ),
                    )
                    setattr(obj, prop, placement)

                elif isinstance(getattr(obj, prop), FreeCAD.Vector) and isinstance(
                    val, dict
                ):
                    vector = FreeCAD.Vector(
                        val.get("x", 0), val.get("y", 0), val.get("z", 0)
                    )
                    setattr(obj, prop, vector)

                elif prop in ["Base", "Tool", "Source", "Profile"] and isinstance(
                    val, str
                ):
                    ref_obj = doc.getObject(val)
                    if ref_obj:
                        setattr(obj, prop, ref_obj)
                    else:
                        raise ValueError(f"Referenced object '{val}' not found.")

                elif prop == "References" and isinstance(val, list):
                    refs = []
                    for ref_name, face in val:
                        ref_obj = doc.getObject(ref_name)
                        if ref_obj:
                            refs.append((ref_obj, face))
                        else:
                            raise ValueError(f"Referenced object '{ref_name}' not found.")
                    setattr(obj, prop, refs)

                else:
                    setattr(obj, prop, val)
            # ShapeColor is a property of the ViewObject
            elif prop == "ShapeColor" and isinstance(val, (list, tuple)):
                setattr(obj.ViewObject, prop, (float(val[0]), float(val[1]), float(val[2]), float(val[3])))

            elif prop == "ViewObject" and isinstance(val, dict):
                for k, v in val.items():
                    if k == "ShapeColor":
                        setattr(obj.ViewObject, k, (float(v[0]), float(v[1]), float(v[2]), float(v[3])))
                    else:
                        setattr(obj.ViewObject, k, v)

            else:
                setattr(obj, prop, val)

        except Exception as e:
            FreeCAD.Console.PrintError(f"Property '{prop}' assignment error: {e}\n")


def start_rpc_server(host="localhost", port=9875):
    global rpc_server_instance, rpc_server_thread
    if rpc_server_instance:
        return "RPC Server already running."
    tool_mods = {}
    tools_available = []
    base_path = os.path.dirname(os.path.abspath(__file__))
    for root, _, files in os.walk(os.path.join(base_path, 'tools')):
        for file in files:
            nam, ext = os.path.splitext(file)
            if ext == '.py' and nam != '__init__':
                mod, _ = os.path.splitext(os.path.relpath(os.path.join(root, file), start=os.path.dirname(base_path)))
                print('mod', mod)
                components = mod.split('/')
                module = ""
                tool = ""
                for c in range(len(components)):
                    module = module + components[c]
                    if c > 1:
                        tool = tool + components[c]
                        if c < len(components) - 1:
                            tool = tool + "-"
                    if c < len(components) - 1:
                        module = module + "."
                print('module', module)
                print('tool', tool)
                tool_mods[tool] = importlib.import_module(module)
                tools_available.append(tool_mods[tool].tool_type)
    tool_names = [t.name for t in tools_available]

    rpc_server_instance = Server('FreeCAD-MCP')

    @rpc_server_instance.call_tool()
    async def call_tool(
        name: str, arguments: dict
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        if name in tool_names:
            return tool_mods[name].do_it(arguments)
        else:
            raise ValueError(f"Unknown tool {name}")

    @rpc_server_instance.list_tools()
    async def list_tools() -> list[types.Tool]:
        return tools_available

    sse = SseServerTransport("/messages/")

    async def handle_sse(request):
        async with sse.connect_sse(
            request.scope, request.receive, request._send
        ) as streams:
            await rpc_server_instance.run(
                streams[0], streams[1], rpc_server_instance.create_initialization_options()
            )
        return Response()

    starlette_app = Starlette(
        debug=True,
        routes=[
            Route("/sse", endpoint=handle_sse, methods=["GET"]),
            Mount("/messages/", app=sse.handle_post_message),
        ],
    )

    def server_loop():
        FreeCAD.Console.PrintMessage(f"RPC Server started at {host}:{port}\n")
        uvicorn.run(starlette_app, host="0.0.0.0", port=port)

    rpc_server_thread = threading.Thread(target=server_loop, daemon=True)
    rpc_server_thread.start()
    
    QtCore.QTimer.singleShot(500, process_gui_tasks)

    return f"RPC Server started at {host}:{port}."


def stop_rpc_server():
    global rpc_server_instance, rpc_server_thread

    if rpc_server_instance:
        rpc_server_thread.join()
        sse_server_instance = None
        rpc_server_thread = None
        FreeCAD.Console.PrintMessage("RPC Server stopped.\n")
        return "RPC Server stopped."

    return "RPC Server was not running."


class StartRPCServerCommand:
    def GetResources(self):
        return {"MenuText": "Start RPC Server", "ToolTip": "Start RPC Server"}

    def Activated(self):
        msg = start_rpc_server()
        FreeCAD.Console.PrintMessage(msg + "\n")

    def IsActive(self):
        return True


class StopRPCServerCommand:
    def GetResources(self):
        return {"MenuText": "Stop RPC Server", "ToolTip": "Stop RPC Server"}

    def Activated(self):
        msg = stop_rpc_server()
        FreeCAD.Console.PrintMessage(msg + "\n")

    def IsActive(self):
        return True


FreeCADGui.addCommand("Start_RPC_Server", StartRPCServerCommand())
FreeCADGui.addCommand("Stop_RPC_Server", StopRPCServerCommand())