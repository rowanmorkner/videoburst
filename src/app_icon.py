#!/usr/bin/env python3
"""
Create a simple app icon for the Slideshow Creator
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # Create icon in multiple sizes
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    img_files = []
    
    for size in sizes:
        # Create a new image with a black background
        img = Image.new('RGBA', (size, size), color=(42, 42, 46, 255))
        draw = ImageDraw.Draw(img)
        
        # Calculate center and radius
        center = size // 2
        radius = int(size * 0.35)
        
        # Draw a play button triangle
        triangle_points = [
            (center - int(radius * 0.8), center - radius),
            (center - int(radius * 0.8), center + radius),
            (center + radius, center)
        ]
        draw.polygon(triangle_points, fill=(240, 80, 120, 255))
        
        # Save as PNG
        filename = f"icon_{size}x{size}.png"
        img.save(filename)
        img_files.append(filename)
        
    # Convert to icns using iconutil (macOS tool)
    # First create iconset directory
    os.makedirs("app.iconset", exist_ok=True)
    
    # Copy files into iconset with required names
    for size, filename in zip(sizes, img_files):
        if size <= 512:  # Standard sizes
            os.system(f"cp {filename} app.iconset/icon_{size}x{size}.png")
            # Retina display (@2x) versions
            if size * 2 in sizes:
                os.system(f"cp icon_{size*2}x{size*2}.png app.iconset/icon_{size}x{size}@2x.png")
    
    # Use iconutil to create icns file
    os.system("iconutil -c icns app.iconset")
    
    # Clean up temporary files
    for filename in img_files:
        os.remove(filename)
    os.system("rm -rf app.iconset")
    
    print("Created app.icns icon file")

if __name__ == "__main__":
    create_icon()