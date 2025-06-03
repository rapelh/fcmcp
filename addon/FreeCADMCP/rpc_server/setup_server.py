import FreeCAD
import FreeCADGui
import shutil
import subprocess
import sys

def init_rpc_server():
    subprocess.check_call([shutil.which("pip"), "install", "mcp", "-U"])
    return "RPC Server packages installed/upgraded."

class InitRPCServerCommand:
    def GetResources(self):
        return {"MenuText": "Init RPC Server", "ToolTip": "Init RPC Server"}

    def Activated(self):
        msg = init_rpc_server()
        FreeCAD.Console.PrintMessage(msg + "\n")

    def IsActive(self):
        return True

FreeCADGui.addCommand("Init_RPC_Server", InitRPCServerCommand())
