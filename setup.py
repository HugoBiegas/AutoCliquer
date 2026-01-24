"""Setup script for cx_Freeze"""
import sys
from cx_Freeze import setup, Executable

# Dependencies
build_exe_options = {
    "packages": [
        "customtkinter",
        "pyautogui",
        "pynput",
        "keyboard",
        "tkinter",
        "json",
        "threading",
        "time",
        "os",
        "sys",
        "socket",
    ],
    "includes": [
        "pynput.keyboard._win32",
        "pynput.mouse._win32",
    ],
    "include_files": [
        ("assets/icon.ico", "assets/icon.ico"),
        ("src", "src"),
    ],
    "excludes": ["unittest", "email", "xml", "pydoc"],
}

# Executable configuration
base = "Win32GUI" if sys.platform == "win32" else None

executables = [
    Executable(
        "main.py",
        base=base,
        target_name="AutoClicker.exe",
        icon="assets/icon.ico",
    )
]

setup(
    name="AutoClicker",
    version="1.0.0",
    description="Auto-Clicker avec mode script",
    options={"build_exe": build_exe_options},
    executables=executables,
)
