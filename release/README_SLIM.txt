VideoBurst: Fast Slideshow Creator (Slim Version)
==============================================

This is the optimized version of VideoBurst, a streamlined application for creating rapid-fire slideshows.
The slim version has been optimized to reduce size while maintaining all core functionality.

Contents:
---------
- macos/ - Contains optimized macOS application
- windows/ - Windows executable (will be added in future releases)

Size Optimizations:
------------------
- Removed unnecessary Python libraries (pandas, matplotlib, etc.)
- Streamlined core image processing code
- Optimized PyInstaller packaging with bytecode optimization
- Reduced dependency footprint

Installation:
------------

macOS:
1. Download the VideoBurst-macOS-slim.zip file from the release page
2. Unzip the downloaded file
3. Drag the "Slideshow Creator Slim.app" to your Applications folder
4. Right-click and select "Open" the first time you run it (to bypass macOS security)

Windows:
1. Download the VideoBurst-Windows-slim.zip file (when available)
2. Unzip the downloaded file
3. Run the "Slideshow Creator Slim.exe" executable

Requirements:
------------
- FFmpeg is required and must be installed separately if not already on your system
  - macOS: Install via Homebrew with 'brew install ffmpeg'
  - Windows: Download from https://ffmpeg.org/download.html

For more information, see the full documentation at:
https://github.com/rowanmorkner/videoburst

Questions or issues? Submit them at:
https://github.com/rowanmorkner/videoburst/issues