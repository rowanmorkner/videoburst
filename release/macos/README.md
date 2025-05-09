# VideoBurst for macOS - Streamlined App Version

This folder contains the optimized version of VideoBurst for macOS.

## About the Optimized Version

The application has been optimized to reduce its size while maintaining all core functionality. This version:

1. Eliminates unnecessary dependencies
2. Removes unused libraries and modules
3. Streamlines core processing code
4. Reduces binary size through PyInstaller optimizations

## Installation

1. Download the [VideoBurst-macOS-slim.zip](https://github.com/rowanmorkner/videoburst/releases/latest) file from the releases page
2. Unzip the downloaded file
3. Drag the "Slideshow Creator Slim.app" to your Applications folder
4. Right-click and select "Open" the first time you run it (to bypass macOS security)

## Building Locally

If you prefer to build the app locally:

```bash
# Install required dependencies
pip install -r requirements.txt
pip install pyinstaller

# Generate app icon 
python app_icon.py

# Build optimized app
pyinstaller -y --clean --windowed --icon=app.icns --optimize=2 --exclude-module=pandas --exclude-module=matplotlib --exclude-module=IPython --exclude-module=zmq --exclude-module=scipy --exclude-module=notebook --exclude-module=lxml --name="Slideshow Creator Slim" slideshow_app_slim.py
```

## Requirements

- macOS 10.15 or higher
- FFmpeg (must be installed separately, e.g., via Homebrew with `brew install ffmpeg`)

## Notes

- The optimized version has been verified to work correctly with all core functionality
- This app has been reduced from over 200MB to under 90MB to make distribution more efficient