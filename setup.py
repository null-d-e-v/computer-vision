import sys
from cx_Freeze import setup, Executable


base = None

if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="object detection",
    version="0.0.1",
    description="simple app detection with match template function",
    executables=[Executable("detection_app.py", base=base)],
)
