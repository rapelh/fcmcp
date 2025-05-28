import FreeCAD
import FreeCADGui
import ObjectsFem

import contextlib
import queue
import base64
import io
import importlib
import os
import tempfile
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

from .parts_library import get_parts_list, insert_part_from_library
from .serialize import serialize_object

sse_server_instance = None
sse_server_thread = None

# GUI task queue
sse_request_queue = queue.Queue()
sse_response_queue = queue.Queue()

# async def do_get_version(
# ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
#     result = []
#     print(FreeCAD.Version())
#     result.append(types.TextContent(type="text", text=" ".join(FreeCAD.Version())))
#     #result.append(types.TextContent(type="text", text=str(gui_available)))
#     return result

# async def do_create_document(
#     name: str,
# ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
#     doc = FreeCAD.newDocument(name)
#     return [types.TextContent(type="text", text=doc.Name)]

def process_gui_tasks():
    while not sse_request_queue.empty():
        task = sse_request_queue.get()
        res = task()
        if res is not None:
            sse_response_queue.put(res)
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


class FreeCADSSE:
    """SSE server for FreeCAD"""

    def ping(self):
        return True

    # def create_document(self, name="New_Document"):
    #     print('SSE Server in FreeCADSSE create_document')
    #     sse_request_queue.put(lambda: self._create_document_gui(name))
    #     res = sse_response_queue.get()
    #     if res is True:
    #         return [types.TextContent(type="text", text=name)]
    #     else:
    #         return [types.TextContent(type="text", text=res)]

    # def create_object(self, doc_name, obj_data: dict[str, Any]):
    #     obj = Object(
    #         name=obj_data.get("Name", "New_Object"),
    #         type=obj_data["Type"],
    #         analysis=obj_data.get("Analysis", None),
    #         properties=obj_data.get("Properties", {}),
    #     )
    #     sse_request_queue.put(lambda: self._create_object_gui(doc_name, obj))
    #     res = sse_response_queue.get()
    #     if res is True:
    #         return [types.TextContent(type="text", text=obj.name)]
    #     else:
    #         return [types.TextContent(type="text", text=res)]

    # def edit_object(self, doc_name: str, obj_name: str, properties: dict[str, Any]) -> dict[str, Any]:
    #     obj = Object(
    #         name=obj_name,
    #         properties=properties.get("Properties", {}),
    #     )
    #     sse_request_queue.put(lambda: self._edit_object_gui(doc_name, obj))
    #     res = sse_response_queue.get()
    #     if res is True:
    #         return [types.TextContent(type="text", text=obj.name)]
    #     else:
    #         return [types.TextContent(type="text", text=res)]

    # def delete_object(self, doc_name: str, obj_name: str):
    #     sse_request_queue.put(lambda: self._delete_object_gui(doc_name, obj_name))
    #     res = sse_response_queue.get()
    #     if res is True:
    #         return [types.TextContent(type="text", text=obj_name)]
    #     else:
    #         return [types.TextContent(type="text", text=res)]

    # def execute_code(self, code: str) -> dict[str, Any]:
    #     output_buffer = io.StringIO()
    #     def task():
    #         try:
    #             with contextlib.redirect_stdout(output_buffer):
    #                 exec(code, globals())
    #             FreeCAD.Console.PrintMessage("Python code executed successfully.\n")
    #             return True
    #         except Exception as e:
    #             FreeCAD.Console.PrintError(
    #                 f"Error executing Python code: {e}\n"
    #             )
    #             return f"Error executing Python code: {e}\n"

    #     sse_request_queue.put(task)
    #     res = sse_response_queue.get()
    #     if res is True:
    #         message = "Python code execution scheduled. \nOutput: " + output_buffer.getvalue()
    #         return [types.TextContent(type="text", text=message)]
    #     else:
    #         return [types.TextContent(type="text", text=res)]


    def get_objects(self, doc_name):
        doc = FreeCAD.getDocument(doc_name)
        if doc:
            return [serialize_object(obj) for obj in doc.Objects]
        else:
            return []

    def get_object(self, doc_name, obj_name):
        doc = FreeCAD.getDocument(doc_name)
        if doc:
            return serialize_object(doc.getObject(obj_name))
        else:
            return None

    # def insert_part_from_library(self, relative_path):
    #     sse_request_queue.put(lambda: self._insert_part_from_library(relative_path))
    #     res = sse_response_queue.get()
    #     if res is True:
    #         return {"success": True, "message": "Part inserted from library."}
    #     else:
    #         return {"success": False, "error": res}

    def list_documents(self):
        return list(FreeCAD.listDocuments().keys())

    def get_parts_list(self):
        return get_parts_list()

    # def get_active_screenshot(self, view_name: str = "Isometric") -> str:
    #     """Get a screenshot of the active view.
        
    #     Returns a base64-encoded string of the screenshot or None if a screenshot
    #     cannot be captured (e.g., when in TechDraw or Spreadsheet view).
    #     """
    #     # First check if the active view supports screenshots
    #     def check_view_supports_screenshots():
    #         try:
    #             active_view = FreeCADGui.ActiveDocument.ActiveView
    #             if active_view is None:
    #                 FreeCAD.Console.PrintWarning("No active view available\n")
    #                 return False
                
    #             view_type = type(active_view).__name__
    #             has_save_image = hasattr(active_view, 'saveImage')
    #             FreeCAD.Console.PrintMessage(f"View type: {view_type}, Has saveImage: {has_save_image}\n")
    #             return has_save_image
    #         except Exception as e:
    #             FreeCAD.Console.PrintError(f"Error checking view capabilities: {e}\n")
    #             return False
                
    #     sse_request_queue.put(check_view_supports_screenshots)
    #     supports_screenshots = sse_response_queue.get()
        
    #     if not supports_screenshots:
    #         FreeCAD.Console.PrintWarning("Current view does not support screenshots\n")
    #         return [types.TextContent(type="text", text="Current view does not support screenshots\n")]
            
    #     # If view supports screenshots, proceed with capture
    #     fd, tmp_path = tempfile.mkstemp(suffix=".png")
    #     os.close(fd)
    #     sse_request_queue.put(
    #         lambda: self._save_active_screenshot(tmp_path, view_name)
    #     )
    #     res = sse_response_queue.get()
    #     if res is True:
    #         try:
    #             with open(tmp_path, "rb") as image_file:
    #                 image_bytes = image_file.read()
    #                 encoded = base64.b64encode(image_bytes).decode("utf-8")
    #         finally:
    #             pass
    #             if os.path.exists(tmp_path):
    #                 os.remove(tmp_path)
    #         return [types.ImageContent(type="image", data=encoded, mimeType="image/png")]
    #     else:
    #         if os.path.exists(tmp_path):
    #             os.remove(tmp_path)
    #         FreeCAD.Console.PrintWarning(f"Failed to capture screenshot: {res}\n")
    #         return [types.TextContent(type="text", text=res)]

    # def _create_document_gui(self, name):
    #     print('SSE Server in FreeCADSSE _create_document_gui')
    #     doc = FreeCAD.newDocument(name)
    #     doc.recompute()
    #     FreeCAD.Console.PrintMessage(f"Document '{name}' created via SSE.\n")
    #     return True

    # def _create_object_gui(self, doc_name, obj: Object):
    #     doc = FreeCAD.getDocument(doc_name)
    #     if doc:
    #         try:
    #             if obj.type == "Fem::FemMeshGmsh" and obj.analysis:
    #                 from femmesh.gmshtools import GmshTools
    #                 res = getattr(doc, obj.analysis).addObject(ObjectsFem.makeMeshGmsh(doc, obj.name))[0]
    #                 if "Part" in obj.properties:
    #                     target_obj = doc.getObject(obj.properties["Part"])
    #                     if target_obj:
    #                         res.Part = target_obj
    #                     else:
    #                         raise ValueError(f"Referenced object '{obj.properties['Part']}' not found.")
    #                     del obj.properties["Part"]
    #                 else:
    #                     raise ValueError("'Part' property not found in properties.")

    #                 for param, value in obj.properties.items():
    #                     if hasattr(res, param):
    #                         setattr(res, param, value)
    #                 doc.recompute()

    #                 gmsh_tools = GmshTools(res)
    #                 gmsh_tools.create_mesh()
    #                 FreeCAD.Console.PrintMessage(
    #                     f"FEM Mesh '{res.Name}' generated successfully in '{doc_name}'.\n"
    #                 )
    #             elif obj.type.startswith("Fem::"):
    #                 fem_make_methods = {
    #                     "MaterialCommon": ObjectsFem.makeMaterialSolid,
    #                     "AnalysisPython": ObjectsFem.makeAnalysis,
    #                 }
    #                 obj_type_short = obj.type.split("::")[1]
    #                 method_name = "make" + obj_type_short
    #                 make_method = fem_make_methods.get(obj_type_short, getattr(ObjectsFem, method_name, None))

    #                 if callable(make_method):
    #                     res = make_method(doc, obj.name)
    #                     set_object_property(doc, res, obj.properties)
    #                     FreeCAD.Console.PrintMessage(
    #                         f"FEM object '{res.Name}' created with '{method_name}'.\n"
    #                     )
    #                 else:
    #                     raise ValueError(f"No creation method '{method_name}' found in ObjectsFem.")
    #                 if obj.type != "Fem::AnalysisPython" and obj.analysis:
    #                     getattr(doc, obj.analysis).addObject(res)
    #             else:
    #                 res = doc.addObject(obj.type, obj.name)
    #                 set_object_property(doc, res, obj.properties)
    #                 FreeCAD.Console.PrintMessage(
    #                     f"{res.TypeId} '{res.Name}' added to '{doc_name}' via SSE.\n"
    #                 )
 
    #             doc.recompute()
    #             return True
    #         except Exception as e:
    #             return str(e)
    #     else:
    #         FreeCAD.Console.PrintError(f"Document '{doc_name}' not found.\n")
    #         return f"Document '{doc_name}' not found.\n"

    # def _edit_object_gui(self, doc_name: str, obj: Object):
    #     doc = FreeCAD.getDocument(doc_name)
    #     if not doc:
    #         FreeCAD.Console.PrintError(f"Document '{doc_name}' not found.\n")
    #         return f"Document '{doc_name}' not found.\n"

    #     obj_ins = doc.getObject(obj.name)
    #     if not obj_ins:
    #         FreeCAD.Console.PrintError(f"Object '{obj.name}' not found in document '{doc_name}'.\n")
    #         return f"Object '{obj.name}' not found in document '{doc_name}'.\n"

    #     try:
    #         # For Fem::ConstraintFixed
    #         if hasattr(obj_ins, "References") and "References" in obj.properties:
    #             refs = []
    #             for ref_name, face in obj.properties["References"]:
    #                 ref_obj = doc.getObject(ref_name)
    #                 if ref_obj:
    #                     refs.append((ref_obj, face))
    #                 else:
    #                     raise ValueError(f"Referenced object '{ref_name}' not found.")
    #             obj_ins.References = refs
    #             FreeCAD.Console.PrintMessage(
    #                 f"References updated for '{obj.name}' in '{doc_name}'.\n"
    #             )
    #             # delete References from properties
    #             del obj.properties["References"]
    #         set_object_property(doc, obj_ins, obj.properties)
    #         doc.recompute()
    #         FreeCAD.Console.PrintMessage(f"Object '{obj.name}' updated via SSE.\n")
    #         return True
    #     except Exception as e:
    #         return str(e)

    # def _delete_object_gui(self, doc_name: str, obj_name: str):
    #     doc = FreeCAD.getDocument(doc_name)
    #     if not doc:
    #         FreeCAD.Console.PrintError(f"Document '{doc_name}' not found.\n")
    #         return f"Document '{doc_name}' not found.\n"

    #     try:
    #         doc.removeObject(obj_name)
    #         doc.recompute()
    #         FreeCAD.Console.PrintMessage(f"Object '{obj_name}' deleted via SSE.\n")
    #         return True
    #     except Exception as e:
    #         return str(e)

    # def _insert_part_from_library(self, relative_path):
    #     try:
    #         insert_part_from_library(relative_path)
    #         return True
    #     except Exception as e:
    #         return str(e)

    # def _save_active_screenshot(self, save_path: str, view_name: str = "Isometric"):
    #     try:
    #         view = FreeCADGui.ActiveDocument.ActiveView
    #         # Check if the view supports screenshots
    #         if not hasattr(view, 'saveImage'):
    #             return "Current view does not support screenshots"
                
    #         if view_name == "Isometric":
    #             view.viewIsometric()
    #         elif view_name == "Front":
    #             view.viewFront()
    #         elif view_name == "Top":
    #             view.viewTop()
    #         elif view_name == "Right":
    #             view.viewRight()
    #         elif view_name == "Back":
    #             view.viewBack()
    #         elif view_name == "Left":
    #             view.viewLeft()
    #         elif view_name == "Bottom":
    #             view.viewBottom()
    #         elif view_name == "Dimetric":
    #             view.viewDimetric()
    #         elif view_name == "Trimetric":
    #             view.viewTrimetric()
    #         else:
    #             raise ValueError(f"Invalid view name: {view_name}")
    #         view.fitAll()
    #         view.saveImage(save_path, 1)
    #         return True
    #     except Exception as e:
    #         return str(e)


def start_sse_server(host="localhost", port=9875):
    global sse_server_instance, sse_server_thread
    tool_mods = {}
    base_path = os.path.dirname(os.path.abspath(__file__))
    for root, _, files in os.walk(os.path.join(base_path, 'tools')):
        for file in files:
            _, ext = os.path.splitext(file)
            if ext == '.py':
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
    if sse_server_instance:
        return "SSE Server already running."
    fc = FreeCADSSE()
    tools_available = []
            # types.Tool(
            #     name="get_active_screenshot",
            #     description="Get screenshot of active view",
            #     inputSchema={
            #         "type": "object",
            #         "required": ["VName"],
            #         "properties": {
            #             "VName": {
            #                 "type": "string",
            #                 "description": "Viev name",
            #             }
            #         },
            #     },
            # ),
            # types.Tool(
            #     name="insert_part_from_library",
            #     description="Insert part from parts library",
            #     inputSchema={
            #         "type": "object",
            #         "required": ["RPath"],
            #         "properties": {
            #             "RPath": {
            #                 "type": "string",
            #                 "description": "Relative path in part library",
            #             }
            #         },
            #     },
            # ),
            # types.Tool(
            #     name="executecode",
            #     description="Execute code parameter",
            #     inputSchema={
            #         "type": "object",
            #         "required": ["Code"],
            #         "properties": {
            #             "Code": {
            #                 "type": "string",
            #                 "description": "Text of code to execute",
            #             }
            #         },
            #     },
            # ),
            # types.Tool(
            #     name="delete_object",
            #     description="Delete a named object in a named document",
            #     inputSchema={
            #         "type": "object",
            #         "required": ["Doc", "Name"],
            #         "properties": {
            #             "Doc": {
            #                 "type": "string",
            #                 "description": "Name of document the object belongs to",
            #             },
            #             "Name": {
            #                 "type": "string",
            #                 "description": "Name of object to modify",
            #             }
            #         },
            #     },
            # ),
            # types.Tool(
            #     name="app-documentobject-edit",
            #     description="Modify properties of a named object in a named document",
            #     inputSchema={
            #         "type": "object",
            #         "required": ["Doc", "Name"],
            #         "properties": {
            #             "Doc": {
            #                 "type": "string",
            #                 "description": "Name of document the object belongs to",
            #             },
            #             "Name": {
            #                 "type": "string",
            #                 "description": "Name of object to modify",
            #             },
            #             "Length": {
            #                 "type": "float",
            #                 "description": "Length of object to set",
            #             },
            #             "Width": {
            #                 "type": "float",
            #                 "description": "Width of object to set",
            #             },
            #             "Height": {
            #                 "type": "float",
            #                 "description": "Height of object to set",
            #             },
            #             "Radius": {
            #                 "type": "float",
            #                 "description": "Radius of object to set",
            #             }
            #         },
            #     },
            # ),
            # types.Tool(
            #     name="create_object",
            #     description="Create a named object in a named document",
            #     inputSchema={
            #         "type": "object",
            #         "required": ["Doc", "Type", "Name"],
            #         "properties": {
            #             "Doc": {
            #                 "type": "string",
            #                 "description": "Name of document in which to create",
            #             },
            #             "Type": {
            #                 "type": "string",
            #                 "description": "Type of object to create",
            #             }, 
            #             "Name": {
            #                 "type": "string",
            #                 "description": "Name of object to create",
            #             },
            #             "Length": {
            #                 "type": "float",
            #                 "description": "Length of object to create",
            #             },
            #             "Width": {
            #                 "type": "float",
            #                 "description": "Width of object to create",
            #             },
            #             "Height": {
            #                 "type": "float",
            #                 "description": "Height of object to create",
            #             },
            #             "Radius": {
            #                 "type": "float",
            #                 "description": "Radius of object to create",
            #             }
            #         },
            #     },
            # ),
            # types.Tool(
            #     name="create_document",
            #     description="Create a named document and returns its name",
            #     inputSchema={
            #         "type": "object",
            #         "required": ["name"],
            #         "properties": {
            #             "name": {
            #                 "type": "string",
            #                 "description": "Name of document to create",
            #             }
            #         },
            #     },
            # ),
            # types.Tool(
            #     name="app-version",
            #     description="Fetches the FreeCAD version and returns its content",
            #     inputSchema={
            #         "type": "object",
            #         "required": [],
            #         "properties": {}
            #     },
        #     )
        # ]
    tools_available.append(tool_mods['app-version'].tool_type)
    tools_available.append(tool_mods['std-new'].tool_type)
    tools_available.append(tool_mods['app-documentobject-new'].tool_type)
    tools_available.append(tool_mods['app-documentobject-edit'].tool_type)
    tools_available.append(tool_mods['app-documentobject-del'].tool_type)
    tools_available.append(tool_mods['executecode'].tool_type)
    tools_available.append(tool_mods['std-mergeproject-frompartslibrary'].tool_type)
    tools_available.append(tool_mods['std-viewscreenshot'].tool_type)
    tool_names = [t.name for t in tools_available]

    sse_server_instance = Server('freecad-mcp')

    @sse_server_instance.call_tool()
    async def call_tool(
        name: str, arguments: dict
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        if name == "app-version":
            return tool_mods['app-version'].do_it(arguments)
        elif name == "std-new":
            return tool_mods['std-new'].do_it(arguments)
        elif name == "app-documentobject-new":
            return tool_mods['app-documentobject-new'].do_it(arguments)
        elif name == "app-documentobject-edit":
            return tool_mods['app-documentobject-edit'].do_it(arguments)
        elif name == "app-documentobject-del":
            return tool_mods['app-documentobject-del'].do_it(arguments)
        elif name == "executecode":
            return tool_mods['executecode'].do_it(arguments)
        elif name == "std-mergeproject-frompartslibrary":
            return tool_mods['std-mergeproject-frompartslibrary'].do_it(arguments)
        elif name == "std-viewscreenshot":
            return tool_mods['std-viewscreenshot'].do_it(arguments)
        else:
            raise ValueError(f"Unknown tool {name}")

    @sse_server_instance.list_tools()
    async def list_tools() -> list[types.Tool]:
        return tools_available

    sse = SseServerTransport("/messages/")

    async def handle_sse(request):
        async with sse.connect_sse(
            request.scope, request.receive, request._send
        ) as streams:
            await sse_server_instance.run(
                streams[0], streams[1], sse_server_instance.create_initialization_options()
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
        FreeCAD.Console.PrintMessage(f"SSE Server started at {host}:{port}\n")
        uvicorn.run(starlette_app, host="0.0.0.0", port=port)

    sse_server_thread = threading.Thread(target=server_loop, daemon=True)
    sse_server_thread.start()
    
    QtCore.QTimer.singleShot(500, process_gui_tasks)

    return f"SSE Server started at {host}:{port}."


def stop_sse_server():
    global sse_server_instance, sse_server_thread

    if sse_server_instance:
        sse_server_thread.join()
        sse_server_instance = None
        sse_server_thread = None
        FreeCAD.Console.PrintMessage("SSE Server stopped.\n")
        return "SSE Server stopped."

    return "SSE Server was not running."


class StartSSEServerCommand:
    def GetResources(self):
        return {"MenuText": "Start SSE Server", "ToolTip": "Start SSE Server"}

    def Activated(self):
        msg = start_sse_server()
        FreeCAD.Console.PrintMessage(msg + "\n")

    def IsActive(self):
        return True


class StopSSEServerCommand:
    def GetResources(self):
        return {"MenuText": "Stop SSE Server", "ToolTip": "Stop SSE Server"}

    def Activated(self):
        msg = stop_sse_server()
        FreeCAD.Console.PrintMessage(msg + "\n")

    def IsActive(self):
        return True


FreeCADGui.addCommand("Start_SSE_Server", StartSSEServerCommand())
FreeCADGui.addCommand("Stop_SSE_Server", StopSSEServerCommand())