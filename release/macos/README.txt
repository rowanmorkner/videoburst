# macOS Release

The macOS application bundle (VideoBurst-macOS.zip) is not included in the Git repository due to GitHub's 100MB file size limit.

## Building the macOS Application

Follow these steps to build the application locally:

1. Make sure Python 3.6+ is installed
2. Install requirements: `pip install -r requirements.txt`
3. Install PyInstaller: `pip install pyinstaller`
4. Generate app icon: `python src/app_icon.py`
5. Build the application:
   ```
   pyinstaller --windowed --icon=app.icns --name="Slideshow Creator" src/slideshow_app.py --add-data "src/create_slideshow.py:."
   ```
6. The application will be created in the `dist` directory

See the main README.md for more detailed instructions.