#!/usr/bin/env python3
"""
Slideshow Creator GUI Application (Slim Version)

A PyQt implementation of the GUI for the create_slideshow_slim.py script.
Optimized to reduce dependencies and size.
"""

import os
import sys
import threading
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFileDialog, QGroupBox,
    QFormLayout, QMessageBox, QSpinBox, QDoubleSpinBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QObject
from create_slideshow_slim import create_slideshow

class WorkerSignals(QObject):
    """Defines signals available for the worker thread."""
    finished = pyqtSignal(bool, str)  # Success flag, Message

class SlideshowCreatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Slideshow Creator")
        self.setMinimumSize(500, 400)
        
        # Create the central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Directory selection
        dir_layout = QHBoxLayout()
        dir_label = QLabel("Image Directory:")
        self.dir_input = QLineEdit("img")
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_directory)
        
        dir_layout.addWidget(dir_label)
        dir_layout.addWidget(self.dir_input, 1)  # 1 is stretch factor
        dir_layout.addWidget(browse_btn)
        main_layout.addLayout(dir_layout)
        
        # Output file
        output_layout = QHBoxLayout()
        output_label = QLabel("Output File:")
        self.output_input = QLineEdit("slideshow.mp4")
        
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_input, 1)  # 1 is stretch factor
        main_layout.addLayout(output_layout)
        
        # Parameters group
        params_group = QGroupBox("Video Parameters")
        params_layout = QFormLayout()
        
        # Photo duration
        self.photo_duration = QDoubleSpinBox()
        self.photo_duration.setRange(0.01, 10.0)
        self.photo_duration.setValue(0.5)
        self.photo_duration.setSingleStep(0.1)
        self.photo_duration.setSuffix(" sec")
        params_layout.addRow("Photo Duration:", self.photo_duration)
        
        # Fade duration
        self.fade_duration = QDoubleSpinBox()
        self.fade_duration.setRange(0.0, 5.0)
        self.fade_duration.setValue(0.1)
        self.fade_duration.setSingleStep(0.05)
        self.fade_duration.setSuffix(" sec")
        params_layout.addRow("Fade Duration:", self.fade_duration)
        
        # Width
        self.width = QSpinBox()
        self.width.setRange(100, 3840)
        self.width.setValue(1080)
        self.width.setSingleStep(10)
        self.width.setSuffix(" px")
        params_layout.addRow("Width:", self.width)
        
        # Height
        self.height = QSpinBox()
        self.height.setRange(100, 2160)
        self.height.setValue(1920)
        self.height.setSingleStep(10)
        self.height.setSuffix(" px")
        params_layout.addRow("Height:", self.height)
        
        # FPS
        self.fps = QSpinBox()
        self.fps.setRange(1, 120)
        self.fps.setValue(30)
        self.fps.setSuffix(" fps")
        params_layout.addRow("Frames Per Second:", self.fps)
        
        params_group.setLayout(params_layout)
        main_layout.addWidget(params_group)
        
        # Create button
        create_btn = QPushButton("Create Slideshow")
        create_btn.setMinimumHeight(40)
        create_btn.clicked.connect(self.create_slideshow)
        main_layout.addWidget(create_btn)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label)
        
        # Set up the worker signals
        self.worker_signals = WorkerSignals()
        self.worker_signals.finished.connect(self.on_completion)
    
    def browse_directory(self):
        """Open a file dialog to select the image directory"""
        directory = QFileDialog.getExistingDirectory(
            self, "Select Image Directory", os.getcwd()
        )
        if directory:
            self.dir_input.setText(directory)
            # Set default output file location in the same directory
            self.output_input.setText(os.path.join(directory, "slideshow.mp4"))
    
    def validate_inputs(self):
        """Validate user inputs before processing"""
        # Check if directory exists
        dir_path = self.dir_input.text()
        if not os.path.exists(dir_path):
            QMessageBox.critical(self, "Error", f"Image directory does not exist: {dir_path}")
            return False
        
        # Check for image files
        has_images = False
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']:
            import glob
            if glob.glob(os.path.join(dir_path, ext)):
                has_images = True
                break
        
        if not has_images:
            QMessageBox.critical(self, "Error", f"No image files found in directory: {dir_path}")
            return False
        
        return True
    
    def create_slideshow(self):
        """Start slideshow creation in a separate thread"""
        if not self.validate_inputs():
            return
        
        # Update status
        self.status_label.setText("Processing... Please wait.")
        self.status_label.setStyleSheet("color: blue;")
        
        # Disable inputs during processing
        self.set_inputs_enabled(False)
        
        # Run in a separate thread to keep UI responsive
        thread = threading.Thread(target=self.run_slideshow_creation)
        thread.daemon = True
        thread.start()
    
    def run_slideshow_creation(self):
        """Run the slideshow creation in a separate thread"""
        try:
            # Ensure output directory exists
            output_path = self.output_input.text()
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Create the slideshow
            create_slideshow(
                image_dir=self.dir_input.text(),
                output_file=output_path,
                photo_duration=self.photo_duration.value(),
                fade_duration=self.fade_duration.value(),
                width=self.width.value(),
                height=self.height.value(),
                fps=self.fps.value()
            )
            
            # Emit signal for successful completion
            self.worker_signals.finished.emit(True, f"Slideshow created: {output_path}")
        
        except Exception as e:
            # Emit signal for error
            self.worker_signals.finished.emit(False, f"Error: {str(e)}")
    
    def on_completion(self, success, message):
        """Handle the completion of slideshow creation"""
        # Update status
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"color: {'green' if success else 'red'};")
        
        # Re-enable inputs
        self.set_inputs_enabled(True)
        
        # Show message box
        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.critical(self, "Error", message)
    
    def set_inputs_enabled(self, enabled):
        """Enable or disable all input widgets"""
        self.dir_input.setEnabled(enabled)
        self.output_input.setEnabled(enabled)
        self.photo_duration.setEnabled(enabled)
        self.fade_duration.setEnabled(enabled)
        self.width.setEnabled(enabled)
        self.height.setEnabled(enabled)
        self.fps.setEnabled(enabled)
        
        # Also enable/disable buttons
        for button in self.findChildren(QPushButton):
            button.setEnabled(enabled)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SlideshowCreatorApp()
    window.show()
    sys.exit(app.exec())