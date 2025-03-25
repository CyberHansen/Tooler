"""
Image Converter module - separated from GUI for better performance
"""
import os
from PIL import Image

def convert_image(input_path, output_format):
    """Convert an image to the specified format"""
    try:
        if not os.path.exists(input_path):
            return False, "Input file does not exist."
        
        # Get the directory and filename without extension
        directory, filename = os.path.split(input_path)
        filename_without_ext = os.path.splitext(filename)[0]
        
        # Create the output path with the new extension
        output_path = os.path.join(directory, f"{filename_without_ext}.{output_format}")
        
        # Open and convert the image
        with Image.open(input_path) as img:
            # Convert to RGB if saving as JPEG and image has transparency
            if output_format.lower() == "jpeg" and img.mode == "RGBA":
                img = img.convert("RGB")
            
            # Save with the new format
            img.save(output_path, format=output_format.upper())
        
        return True, output_path
    
    except Exception as e:
        return False, f"Error converting image: {str(e)}"

def delete_file(file_path):
    """Delete a file from the filesystem"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True, "File deleted successfully."
        else:
            return False, "File does not exist."
    except Exception as e:
        return False, f"Error deleting file: {str(e)}"
