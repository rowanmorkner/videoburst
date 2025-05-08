#!/usr/bin/env python3
"""
VideoBurst runner script - launches the GUI application
"""
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the application
from slideshow_app import SlideshowCreatorApp, QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SlideshowCreatorApp()
    window.show()
    sys.exit(app.exec())