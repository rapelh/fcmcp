import mcp.types as types
import FreeCAD
import FreeCADGui
import base64
import os
import tempfile
from sse_server.sse_server import sse_request_queue, sse_response_queue

tool_type = types.Tool(
                name="Std-ViewScreenshot",
                description="Get screenshot of active view",
                inputSchema={
                    "type": "object",
                    "required": ["VName"],
                    "properties": {
                        "ViewName": {
                            "type": "string",
                            "description": "Viev name",
                        }
                    },
                },
            )

#def get_active_screenshot(view_name: str = "Isometric") -> str:
def do_it(args):
    """Get a screenshot of the active view.
        
    Returns a base64-encoded string of the screenshot or None if a screenshot
    cannot be captured (e.g., when in TechDraw or Spreadsheet view).
    """
    view_name = args.get('ViewName')

    # First check if the active view supports screenshots
    def check_view_supports_screenshots():
        try:
            active_view = FreeCADGui.ActiveDocument.ActiveView
            if active_view is None:
                FreeCAD.Console.PrintWarning("No active view available\n")
                return False
                
            view_type = type(active_view).__name__
            has_save_image = hasattr(active_view, 'saveImage')
            FreeCAD.Console.PrintMessage(f"View type: {view_type}, Has saveImage: {has_save_image}\n")
            return has_save_image
        except Exception as e:
            FreeCAD.Console.PrintError(f"Error checking view capabilities: {e}\n")
            return False
                
    sse_request_queue.put(check_view_supports_screenshots)
    supports_screenshots = sse_response_queue.get()
        
    if not supports_screenshots:
        FreeCAD.Console.PrintWarning("Current view does not support screenshots\n")
        return [types.TextContent(type="text", text="Current view does not support screenshots\n")]
            
    # If view supports screenshots, proceed with capture
    fd, tmp_path = tempfile.mkstemp(suffix=".png")
    os.close(fd)
    sse_request_queue.put(
        lambda: _save_active_screenshot(tmp_path, view_name)
    )
    res = sse_response_queue.get()
    if res is True:
        try:
            with open(tmp_path, "rb") as image_file:
                image_bytes = image_file.read()
                encoded = base64.b64encode(image_bytes).decode("utf-8")
        finally:
            pass
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        return [types.ImageContent(type="image", data=encoded, mimeType="image/png")]
    else:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        FreeCAD.Console.PrintWarning(f"Failed to capture screenshot: {res}\n")
        return [types.TextContent(type="text", text=res)]


def _save_active_screenshot(save_path: str, view_name: str = "Isometric"):
    try:
        view = FreeCADGui.ActiveDocument.ActiveView
        # Check if the view supports screenshots
        if not hasattr(view, 'saveImage'):
            return "Current view does not support screenshots"
                
        if view_name == "Isometric":
            view.viewIsometric()
        elif view_name == "Front":
            view.viewFront()
        elif view_name == "Top":
            view.viewTop()
        elif view_name == "Right":
            view.viewRight()
        elif view_name == "Back":
            view.viewBack()
        elif view_name == "Left":
            view.viewLeft()
        elif view_name == "Bottom":
            view.viewBottom()
        elif view_name == "Dimetric":
            view.viewDimetric()
        elif view_name == "Trimetric":
            view.viewTrimetric()
        else:
            raise ValueError(f"Invalid view name: {view_name}")
        view.fitAll()
        view.saveImage(save_path, 1)
        return True
    except Exception as e:
        return str(e)
