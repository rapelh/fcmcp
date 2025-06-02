import mcp.types as types
import FreeCAD
import json
from rpc_server.rpc_server import rpc_request_queue, rpc_response_queue, set_object_property, Object
from rpc_server.serialize import serialize_object

tool_type = types.Tool(
                name="App-DocumentObject-New",
                description="Create a named object in a named document",
                inputSchema={
                    "type": "object",
                    "required": ["Doc", "Type", "Name"],
                    "properties": {
                        "Doc": {
                            "type": "string",
                            "description": "Name of document in which to create",
                        },
                        "Type": {
                            "type": "string",
                            "description": "Type of object to create",
                        }, 
                        "Name": {
                            "type": "string",
                            "description": "Name of object to create",
                        },
                        "Length": {
                            "type": "number",
                            "description": "Length of object to create",
                        },
                        "Width": {
                            "type": "number",
                            "description": "Width of object to create",
                        },
                        "Height": {
                            "type": "number",
                            "description": "Height of object to create",
                        },
                        "Radius": {
                            "type": "number",
                            "description": "Radius of object to create",
                        }
                    },
                },
            )

def do_it(args):
    doc_name = args.get("Doc")
    obj = Object(
        name=args.get("Name", "New_Object"),
        type=args["Type"],
        analysis=args.get("Analysis", None),
        properties=args.get("Properties", {}),
    )
    rpc_request_queue.put(lambda: _create_object_gui(doc_name, obj))
    res, text = rpc_response_queue.get()
    if res is True:
        return [types.TextContent(type="text", text=text)]
    else:
        return [types.TextContent(type="text", text=text)]

def _create_object_gui(doc_name, obj: Object):
    doc = FreeCAD.getDocument(doc_name)
    if doc:
        try:
            if obj.type == "Fem::FemMeshGmsh" and obj.analysis:
                from femmesh.gmshtools import GmshTools
                res = getattr(doc, obj.analysis).addObject(ObjectsFem.makeMeshGmsh(doc, obj.name))[0]
                if "Part" in obj.properties:
                    target_obj = doc.getObject(obj.properties["Part"])
                    if target_obj:
                        res.Part = target_obj
                    else:
                        raise ValueError(f"Referenced object '{obj.properties['Part']}' not found.")
                    del obj.properties["Part"]
                else:
                    raise ValueError("'Part' property not found in properties.")

                for param, value in obj.properties.items():
                    if hasattr(res, param):
                        setattr(res, param, value)
                doc.recompute()

                gmsh_tools = GmshTools(res)
                gmsh_tools.create_mesh()
                FreeCAD.Console.PrintMessage(
                    f"FEM Mesh '{res.Name}' generated successfully in '{doc_name}'.\n"
                )
            elif obj.type.startswith("Fem::"):
                fem_make_methods = {
                    "MaterialCommon": ObjectsFem.makeMaterialSolid,
                    "AnalysisPython": ObjectsFem.makeAnalysis,
                }
                obj_type_short = obj.type.split("::")[1]
                method_name = "make" + obj_type_short
                make_method = fem_make_methods.get(obj_type_short, getattr(ObjectsFem, method_name, None))

                if callable(make_method):
                    res = make_method(doc, obj.name)
                    set_object_property(doc, res, obj.properties)
                    FreeCAD.Console.PrintMessage(
                        f"FEM object '{res.Name}' created with '{method_name}'.\n"
                    )
                else:
                    raise ValueError(f"No creation method '{method_name}' found in ObjectsFem.")
                if obj.type != "Fem::AnalysisPython" and obj.analysis:
                    getattr(doc, obj.analysis).addObject(res)
            else:
                res = doc.addObject(obj.type, obj.name)
                set_object_property(doc, res, obj.properties)
                FreeCAD.Console.PrintMessage(
                    f"{res.TypeId} '{res.Name}' added to '{doc_name}' via RPC.\n"
                )
 
            doc.recompute()
            return True, json.dumps(serialize_object(res))
        except Exception as e:
            return False, str(e)
    else:
        FreeCAD.Console.PrintError(f"Document '{doc_name}' not found.\n")
        return False, f"Document '{doc_name}' not found.\n"
