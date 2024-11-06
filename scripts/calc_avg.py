import os
import json
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

# Define the base directory
base_dir = './games/'

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        if 'config.json' in files:
            config_path = os.path.join(root, 'config.json')
            
            # Skip updating config.json if it is directly in the base_files directory
            if 'base_files' in root and root.count(os.sep) == base_dir.count(os.sep) + 1:
                continue
            
            # Initialize variables to calculate average dimensions
            total_width = 0
            total_height = 0
            image_count = 0
            
            # Loop through files to find image files (including .webp)
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')):
                    image_path = os.path.join(root, file)
                    try:
                        with Image.open(image_path) as img:
                            width, height = img.size
                            total_width += width
                            total_height += height
                            image_count += 1
                    except Exception as e:
                        print(f"Error processing image {image_path}: {e}")
            
            # Calculate the average size if images were found
            if image_count > 0:
                average_width = total_width // image_count
                average_height = total_height // image_count
                average_size = {"x": average_width, "y": average_height}
                
                # Read and update the config.json file
                with open(config_path, 'r+', encoding='utf-8') as config_file:
                    config_data = json.load(config_file)
                    config_data['average_size'] = average_size
                    
                    # Write the updated data back to config.json
                    config_file.seek(0)
                    json.dump(config_data, config_file, indent=4)
                    config_file.truncate()
                    
                print(f"Updated {config_path} with average size: {average_size}")
            else:
                print(f"No images found in {root}")

        # If the directory contains "base_files", process its subdirectories
        if 'base_files' in root:
            for sub_dir in dirs:
                process_directory(os.path.join(root, sub_dir))

# Start processing from the base directory
process_directory(base_dir)
