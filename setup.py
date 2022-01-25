import sys
from cx_Freeze import setup, Executable
from importlib_metadata import version


base = "Win32GUI"

setup(
    name="object detection",
    version="0.0.1",
    description="simple app detection with match template function",
    executables=[Executable("detection_app.py", base=base)],
)
