import os
import json
from PIL import Image
import re
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
            
            # Initialize dimensions directory
            sizes_dict = {}
            image_count = 0
            
            # Loop through files to find image files (including .webp)
            with open(config_path, "rt", encoding="utf-8") as config_file:
                config = json.loads(config_file.read())
                scaling = config.get("rescaling_factor", {})
                regex_str = config.get("prefix", "") + "(.*)" + config.get("postfix", "") + "(.*)\\.([A-Za-z0-9]*)"
                regex = re.compile(regex_str)
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')):
                    image_path = os.path.join(root, file)
                    image_name = os.path.basename(image_path)
                    regex_search = regex.search(image_name)
                    if not regex_search:
                        print(f"Error processing image {image_path}: Image name did not match config")
                    else:
                        codename, index = regex_search.group(1), regex_search.group(2)
                        if index:
                            index = str(int(index))
                        else:
                            index = "null"
                        try:
                            with Image.open(image_path) as img:
                                width, height = img.size
                                if codename in sizes_dict.keys():
                                    sizes_dict[codename][index] = {
                                        "x": width, "y": height
                                    }
                                else:
                                    sizes_dict[codename] = {
                                        index: {"x": width, "y": height}
                                    }
                                image_count += 1
                            sizes_dict[codename] = dict(sorted(sizes_dict[codename].items()))
                        except Exception as e:
                            print(f"Error processing image {image_path}: {e}")
            
            # Calculate the average size if images were found
            if image_count > 0:
                # Read and update the config.json file
                with open(config_path, 'r+', encoding='utf-8') as config_file:
                    config_data = json.load(config_file)
                    config_data['image_sizes'] = dict(sorted(sizes_dict.items()))
                    
                    # Write the updated data back to config.json
                    config_file.seek(0)
                    json.dump(config_data, config_file, indent=2)
                    config_file.truncate()
                    
                print(f"Updated {config_path} with image dimensions")
            else:
                print(f"No images found in {root}")

        # If the directory contains "base_files", process its subdirectories
        if 'base_files' in root:
            for sub_dir in dirs:
                process_directory(os.path.join(root, sub_dir))

# Start processing from the base directory
process_directory(base_dir)
