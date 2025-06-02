import FreeCAD
from FreeCAD import Base
import Part
import Materials
import json
import sys

sys.setrecursionlimit(2000)

def serialize_value(value):

    if value is None:
        return value
    elif isinstance(value, dict):
        rv = {}
        for k, v in value.items():
            rv[k] = serialize_value(v)
    elif isinstance(value, (int, float, str, bool)):
        return value
    elif isinstance(value, Base.Vector):
        return [v for v in list(value)]
    elif isinstance(value, FreeCAD.Vector):
        return {"x": value.x, "y": value.y, "z": value.z}
    elif isinstance(value, FreeCAD.Rotation):
        return {
            "Axis": {"x": value.Axis.x, "y": value.Axis.y,  "z": value.Axis.z},
            "Angle": value.Angle,
        }
    elif isinstance(value, FreeCAD.Placement):
        return {
            "Base": serialize_value(value.Base),
            "Rotation": serialize_value(value.Rotation),
        }
    elif isinstance(value, (list, tuple)):
        return [serialize_value(v) for v in value]
    elif isinstance(value, object):
        rv = {}
        if hasattr(value, 'ProperiesList'):
            for prop in value.PropertiesList:
                v = value.__getattribute__(prop)
                rv[prop] = serialize_value(v)
        elif hasattr(value, '__dict__'):
            for prop in value.__dict__:
                if prop[0].isupper():
                    v = value.__getattribute__(prop)
                    rv[prop] = serialize_value(v)
        return rv
    else:
        return value


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
    elif isinstance(obj, FreeCAD.Document):
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
                if prop == 'Base':
                    result["Properties"][prop] = serialize_object(getattr(obj, prop))
                else:
                    result["Properties"][prop] = serialize_value(getattr(obj, prop))
            except Exception as e:
                result["Properties"][prop] = f"<error: {str(e)}>"

        if hasattr(obj, "ViewObject") and obj.ViewObject is not None:
            view = obj.ViewObject
            result["ViewObject"] = serialize_view_object(view)

        return result
