#!/usr/bin/env python3
"""
Build script for creating standalone VideoBurst applications
"""
import os
import sys
import platform
import subprocess

# Ensure we're in the correct directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# First, create the app icon
print("Creating application icon...")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from app_icon import create_icon
create_icon()

# Determine platform-specific settings
if platform.system() == "Darwin":  # macOS
    icon_file = "app.icns"
    separator = ":"
elif platform.system() == "Windows":
    icon_file = "app.ico"  # Note: This file would need to be created for Windows
    separator = ";"
else:  # Linux
    icon_file = None
    separator = ":"

# Build command
cmd = [
    "pyinstaller",
    "--clean",
    "--windowed",
    "--name=Slideshow Creator"
]

# Add icon if available
if icon_file and os.path.exists(icon_file):
    cmd.extend(["--icon", icon_file])

# Add data files
cmd.extend([
    f"--add-data=src/create_slideshow.py{separator}.",
    "run.py"
])

# Run the build
print(f"Building application with command: {' '.join(cmd)}")
subprocess.run(cmd, check=True)

print("\nBuild completed! The application can be found in the 'dist' directory.")