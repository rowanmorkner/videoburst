# VideoBurst Installation Guide

This document provides detailed installation instructions for the VideoBurst slideshow creator application.

## macOS Installation

1. Unzip the `VideoBurst-macOS.zip` file located in the `macos` folder
2. Drag the "Slideshow Creator.app" to your Applications folder
3. Right-click on the application and select "Open" the first time you run it (this bypasses macOS security for applications from unidentified developers)

## Windows Installation

1. Unzip the `VideoBurst-Windows.zip` file located in the `windows` folder (when available)
2. Run the "Slideshow Creator.exe" executable
3. You may need to allow the application through your Windows Defender settings

## FFmpeg Requirement

VideoBurst requires FFmpeg to be installed on your system:

### macOS FFmpeg Installation:

1. Install Homebrew if you don't have it already:
   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. Install FFmpeg using Homebrew:
   ```
   brew install ffmpeg
   ```

### Windows FFmpeg Installation:

1. Download FFmpeg from the official website: https://ffmpeg.org/download.html
2. Extract the downloaded archive to a folder (e.g., `C:\ffmpeg`)
3. Add FFmpeg to your system PATH:
   - Right-click on "This PC" or "My Computer" and select "Properties"
   - Click on "Advanced system settings"
   - Click on "Environment Variables"
   - Under "System variables", find and select "Path", then click "Edit"
   - Click "New" and add the path to the FFmpeg bin folder (e.g., `C:\ffmpeg\bin`)
   - Click "OK" to close all dialogs

## Troubleshooting

If you encounter any issues:

1. Ensure FFmpeg is properly installed and available in your system PATH
2. Check that your system meets the minimum requirements
3. For macOS users: If the app won't open, try right-clicking and selecting "Open" instead of double-clicking
4. For Windows users: Try running the application as administrator

For further assistance, please visit the [GitHub Issues page](https://github.com/rowanmorkner/videoburst/issues).