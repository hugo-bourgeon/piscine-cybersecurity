# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    scorpion.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: hubourge <hubourge@student.42angouleme.    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/06/04 16:40:00 by hubourge          #+#    #+#              #
#    Updated: 2025/06/04 16:54:12 by hubourge         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import argparse
import sys
import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import datetime

def parse_args():
    parser = argparse.ArgumentParser(description="Extract EXIF and metadata from image files")
    parser.add_argument("files", 
                        nargs="+")
    return parser.parse_args()

def get_file_info(filepath):
    """Get basic file information"""
    try:
        stat = os.stat(filepath)
        size = stat.st_size
        creation_time = datetime.datetime.fromtimestamp(stat.st_ctime)
        modification_time = datetime.datetime.fromtimestamp(stat.st_mtime)
        
        return {
            'size': size,
            'creation_time': creation_time,
            'modification_time': modification_time
        }
    except Exception as e:
        return None

def extract_exif_data(image_path):
    """Extract EXIF data from image"""
    try:
        with Image.open(image_path) as image:
            # Get basic image info
            image_info = {
                'format': image.format,
                'mode': image.mode,
                'size': image.size
            }
            
            # Get EXIF data
            exif_data = {}
            if hasattr(image, '_getexif') and image._getexif() is not None:
                exif = image._getexif()
                for tag_id, value in exif.items():
                    tag = TAGS.get(tag_id, tag_id)
                    
                    # Handle GPS data specially
                    if tag == "GPSInfo":
                        gps_data = {}
                        for gps_tag_id, gps_value in value.items():
                            gps_tag = GPSTAGS.get(gps_tag_id, gps_tag_id)
                            gps_data[gps_tag] = gps_value
                        exif_data[tag] = gps_data
                    else:
                        exif_data[tag] = value
            
            return image_info, exif_data
            
    except Exception as e:
        return None, None

def format_value(value):
    """Format values for display"""
    if isinstance(value, bytes):
        try:
            return value.decode('utf-8', errors='ignore')
        except:
            return str(value)
    elif isinstance(value, tuple) and len(value) == 2:
        # Handle rational numbers (common in EXIF)
        try:
            return f"{value[0]}/{value[1]}" if value[1] != 0 else str(value[0])
        except:
            return str(value)
    elif isinstance(value, dict):
        return {k: format_value(v) for k, v in value.items()}
    else:
        return str(value)

def display_metadata(filepath):
    """Display all metadata for a file"""
    print(f"\n{'='*60}")
    print(f"File: {filepath}")
    print(f"{'='*60}")
    
    # Check if file exists
    if not os.path.exists(filepath):
        print(f" [Error] File not found: {filepath}")
        return
    
    # Check file extension
    valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
    if not filepath.lower().endswith(valid_extensions):
        print(f" [Error] Unsupported file format. Supported: {', '.join(valid_extensions)}")
        return
    
    # Get file system info
    file_info = get_file_info(filepath)
    if file_info:
        print(f"\nFile Information:")
        print(f"  Size:              {file_info['size']} bytes")
        print(f"  Creation time:     {file_info['creation_time']}")
        print(f"  Modification time: {file_info['modification_time']}")
    
    # Get image and EXIF data
    image_info, exif_data = extract_exif_data(filepath)
    
    if image_info is None:
        print(f" [Error] Could not read image: {filepath}")
        return
    
    # Display image information
    print(f"\nImage Information:")
    print(f"  Format:     {image_info['format']}")
    print(f"  Mode:       {image_info['mode']}")
    print(f"  Dimensions: {image_info['size'][0]}x{image_info['size'][1]} pixels")
    
    # Display EXIF data
    if exif_data:
        print(f"\nEXIF Data:")
        for tag, value in exif_data.items():
            formatted_value = format_value(value)
            if isinstance(formatted_value, dict):
                print(f"  {tag}:")
                for sub_tag, sub_value in formatted_value.items():
                    print(f"    {sub_tag}: {sub_value}")
            else:
                # Truncate very long values
                if len(str(formatted_value)) > 100:
                    formatted_value = str(formatted_value)[:100] + "..."
                print(f"  {tag}: {formatted_value}")
    else:
        print(f"\nNo EXIF data found")

def main():
    args = parse_args()
    
    print(f"Analyzing {len(args.files)} file(s)...")
    
    for filepath in args.files:
        display_metadata(filepath)
    
    print(f"\n{'='*60}")
    print(f"Analysis complete.")

if __name__ == "__main__":
    main()
