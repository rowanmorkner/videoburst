#!/usr/bin/env python3
"""
Slideshow Creator Script (Slim Version)

Creates a rapid-fire slideshow from images in a directory.
- Images displayed in alphabetical order
- Vertical 9:16 format (1080x1920)
- Images scaled to fit width while maintaining aspect ratio
- Optimized to reduce dependencies
"""

import os
import glob
from PIL import Image
import tempfile
import shutil
import subprocess

def create_slideshow(
    image_dir='img',
    output_file='slideshow.mp4',
    photo_duration=0.05,
    fade_duration=0.1,
    width=1080,
    height=1920,
    fps=30
):
    """
    Create a slideshow from images in the specified directory.
    
    Args:
        image_dir (str): Directory containing images
        output_file (str): Output video file name
        photo_duration (float): Duration each photo is displayed in seconds
        fade_duration (float): Duration of crossfade between photos in seconds
        width (int): Width of the output video
        height (int): Height of the output video
        fps (int): Frames per second of the output video
    """
    # Check if image directory exists
    if not os.path.exists(image_dir):
        print(f"Error: Image directory '{image_dir}' not found.")
        return
    
    # Get all image files and sort them alphabetically
    image_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']:
        image_files.extend(glob.glob(os.path.join(image_dir, ext)))
    image_files.sort()
    
    if not image_files:
        print(f"Error: No image files found in '{image_dir}'.")
        return
    
    print(f"Found {len(image_files)} images. Creating slideshow...")
    
    # Create a temporary directory to store processed frames
    temp_dir = tempfile.mkdtemp()
    try:
        frame_count = 0
        
        # Process each image - use enumerate for consistent index
        for img_idx, img_path in enumerate(image_files):
            # Display progress
            print(f"Processing image {img_idx+1}/{len(image_files)}: {os.path.basename(img_path)}")
            
            # Calculate total frames for this image
            image_frames = int(photo_duration * fps)
            
            # Load and process the image
            img = Image.open(img_path)
            
            # Calculate scaling to fit width while maintaining aspect ratio
            img_aspect = img.width / img.height
            target_aspect = width / height
            
            if img_aspect > target_aspect:
                # Image is wider than target in proportion - scale to width
                new_width = width
                new_height = int(width / img_aspect)
            else:
                # Image is taller than target in proportion - scale to width
                new_width = width
                new_height = int(width / img_aspect)
            
            # Resize the image
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Create a black background image
            background = Image.new('RGB', (width, height), (0, 0, 0))
            
            # Calculate position to paste (centered)
            paste_x = (width - new_width) // 2
            paste_y = (height - new_height) // 2
            
            # Paste the image onto the background
            background.paste(img, (paste_x, paste_y))
            
            # Save as frame
            for frame in range(image_frames):
                frame_file = os.path.join(temp_dir, f"frame_{frame_count:06d}.jpg")
                background.save(frame_file, quality=95)
                frame_count += 1
                
            # Add fade frames if this isn't the last image
            if img_idx < len(image_files) - 1:
                # Load next image for crossfade
                next_img = Image.open(image_files[img_idx + 1])
                
                # Process next image
                next_img_aspect = next_img.width / next_img.height
                
                if next_img_aspect > target_aspect:
                    next_new_width = width
                    next_new_height = int(width / next_img_aspect)
                else:
                    next_new_width = width
                    next_new_height = int(width / next_img_aspect)
                
                next_img = next_img.resize((next_new_width, next_new_height), Image.Resampling.LANCZOS)
                
                next_background = Image.new('RGB', (width, height), (0, 0, 0))
                next_paste_x = (width - next_new_width) // 2
                next_paste_y = (height - next_new_height) // 2
                next_background.paste(next_img, (next_paste_x, next_paste_y))
                
                # Create fade frames
                fade_frames = int(fade_duration * fps)
                for f in range(fade_frames):
                    alpha = f / fade_frames  # 0 to 1
                    
                    # Create blended frame
                    blend = Image.blend(background, next_background, alpha)
                    
                    # Save fade frame
                    frame_file = os.path.join(temp_dir, f"frame_{frame_count:06d}.jpg")
                    blend.save(frame_file, quality=95)
                    frame_count += 1
        
        print(f"Generated {frame_count} frames. Creating video...")
        
        # Create video using ffmpeg
        ffmpeg_cmd = [
            'ffmpeg', '-y',
            '-framerate', str(fps),
            '-i', os.path.join(temp_dir, 'frame_%06d.jpg'),
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', '23',
            '-pix_fmt', 'yuv420p',
            output_file
        ]
        
        print(f"Running: {' '.join(ffmpeg_cmd)}")
        subprocess.run(ffmpeg_cmd, check=True)
        
        print(f"Slideshow created successfully: {output_file}")
        print(f"- Duration: {frame_count / fps:.2f} seconds")
        print(f"- Number of images: {len(image_files)}")
        print(f"- Resolution: {width}x{height}")
            
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Create a slideshow from images")
    parser.add_argument("-d", "--directory", default="img", help="Directory containing images (default: img)")
    parser.add_argument("-o", "--output", default="slideshow.mp4", help="Output video file (default: slideshow.mp4)")
    parser.add_argument("-p", "--photo-duration", type=float, default=0.5, help="Duration each photo is displayed in seconds (default: 0.5)")
    parser.add_argument("-f", "--fade-duration", type=float, default=0.1, help="Duration of crossfade between photos in seconds (default: 0.1)")
    parser.add_argument("--width", type=int, default=1080, help="Width of the output video (default: 1080)")
    parser.add_argument("--height", type=int, default=1920, help="Height of the output video (default: 1920)")
    parser.add_argument("--fps", type=int, default=30, help="Frames per second (default: 30)")
    
    args = parser.parse_args()
    
    create_slideshow(
        image_dir=args.directory,
        output_file=args.output,
        photo_duration=args.photo_duration,
        fade_duration=args.fade_duration,
        width=args.width,
        height=args.height,
        fps=args.fps
    )