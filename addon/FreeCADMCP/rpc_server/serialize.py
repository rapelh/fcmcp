import FreeCAD as App
import Part
import Materials
import json
import sys

sys.setrecursionlimit(8000)

def serialize_value(value):
    if isinstance(value, (int, float, str, bool, dict)):
        return value
    elif isinstance(value, Part.Face):
        return {
            "Area": serialize_value(value.Area),
            "BoundBox": serialize_value(value.BoundBox),
            "CenterOfGravity": serialize_value(value.CenterOfGravity),
            "CenterOfMass": serialize_value(value.CenterOfMass),
            "CompSolids": serialize_value(value.CompSolids),
            "Compounds": serialize_value(value.Compounds),
            "Content": serialize_value(value.Content),
            "Edges": serialize_value(value.Edges),
            "ElementMap": serialize_value(value.ElementMap),
            "ElementMapSize": serialize_value(value.ElementMapSize),
            "ElementMapVersion": serialize_value(value.ElementMapVersion),
            "ElementReverseMap": serialize_value(value.ElementReverseMap),
            #"Faces": serialize_value(value.Faces),
            "Hasher": serialize_value(value.Hasher),
            "Length": serialize_value(value.Length),
            "Mass": serialize_value(value.Mass),
            "MatrixOfInertia": serialize_value(value.MatrixOfInertia),
            "MemSize": serialize_value(value.MemSize),
            "Module": serialize_value(value.Module),
            "Orientation": serialize_value(value.Orientation),
            "OuterWire": serialize_value(value.OuterWire),
            "ParameterRange": serialize_value(value.ParameterRange),
            "Placement": serialize_value(value.Placement),
            "PrincipalProperties": serialize_value(value.PrincipalProperties),
            "ShapeType": serialize_value(value.ShapeType),
            "Shells": serialize_value(value.Shells),
            "Solids": serialize_value(value.Solids),
            "StaticMoments": serialize_value(value.StaticMoments),
            "SubShapes": serialize_value(value.SubShapes),
            "Surface": serialize_value(value.Surface),
            "Tag": serialize_value(value.Tag),
            "Tolerance": serialize_value(value.Tolerance),
            "TypeId": serialize_value(value.TypeId),
            "Vertexes": serialize_value(value.Vertexes),
            "Volume": serialize_value(value.Volume),
            "Wire": serialize_value(value.Wire),
            "Wires": serialize_value(value.Wires)          
        }
    elif isinstance(value, Materials.Material):
        return {
            "AppearanceModels": serialize_value(value.AppearanceModels),
            "AppearanceProperties": serialize_value(value.AppearanceProperties),
            "Author": serialize_value(value.Author),
            "AuthorAndLicense": serialize_value(value.AuthorAndLicense),
            "Description": serialize_value(value.Description),
            "Directory": serialize_value(value.Directory),
            "LegacyProperties": serialize_value(value.LegacyProperties),
            "LibraryIcon": serialize_value(value.LibraryIcon),
            "LibraryName": serialize_value(value.LibraryName),
            "LibraryRoot": serialize_value(value.LibraryRoot),
            "License": serialize_value(value.License),
            "Module": serialize_value(value.Module),
            "Name": serialize_value(value.Name),
            "Parent": serialize_value(value.Parent),
            "PhysicalModels": serialize_value(value.PhysicalModels),
            "PhysicalProperties": serialize_value(value.PhysicalProperties),
            "Properties": serialize_value(value.Properties),
            "Reference": serialize_value(value.Reference),
            "Tags": serialize_value(value.Tags),
            "TypeId": serialize_value(value.TypeId),
            "URL": serialize_value(value.URL),
            "UUID": serialize_value(value.UUID)
        }
    elif isinstance(value, App.Vector):
        return {"x": value.x, "y": value.y, "z": value.z}
    elif isinstance(value, App.Rotation):
        return {
            "Axis": {"x": value.Axis.x, "y": value.Axis.y, "z": value.Axis.z},
            "Angle": value.Angle,
        }
    elif isinstance(value, App.Placement):
        return {
            "Base": serialize_value(value.Base),
            "Rotation": serialize_value(value.Rotation),
        }
    elif isinstance(value, (list, tuple)):
        return [serialize_value(v) for v in value]
    #elif isinstance(value, (App.Color)):
    #    return tuple(value)
    else:
        return str(value.__class__)


def serialize_shape(shape):
    if shape is None:
        return None
    return {
        "Volume": shape.Volume,
        "Area": shape.Area,
        "VertexCount": len(shape.Vertexes),
        "EdgeCount": len(shape.Edges),
        "FaceCount": len(shape.Faces),
    }


def serialize_view_object(view):
    if view is None:
        return None
    return {
        "ShapeColor": serialize_value(view.ShapeColor),
        "Transparency": view.Transparency,
        "Visibility": view.Visibility,
    }


def serialize_object(obj):
    if isinstance(obj, list):
        return [serialize_object(item) for item in obj]
    elif isinstance(obj, App.Document):
        return {
            "Name": obj.Name,
            "Label": obj.Label,
            "FileName": obj.FileName,
            "Objects": [serialize_object(child) for child in obj.Objects],
        }
    else:
        result = {
            "Name": obj.Name,
            "Label": obj.Label,
            "TypeId": obj.TypeId,
            "Properties": {},
            "Placement": serialize_value(getattr(obj, "Placement", None)),
            "Shape": serialize_shape(getattr(obj, "Shape", None)),
            "ViewObject": {},
        }

        for prop in obj.PropertiesList:
            try:
                result["Properties"][prop] = serialize_value(getattr(obj, prop))
            except Exception as e:
                result["Properties"][prop] = f"<error: {str(e)}>"

        if hasattr(obj, "ViewObject") and obj.ViewObject is not None:
            view = obj.ViewObject
            result["ViewObject"] = serialize_view_object(view)

        return result
