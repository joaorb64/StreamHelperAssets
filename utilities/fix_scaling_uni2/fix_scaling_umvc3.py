from PIL import Image
from glob import glob
import json
import os.path
from copy import deepcopy

# file_list = glob("../../games/umvc3/base_files/icon/*.png", recursive=True)
with open("../../games/umvc3/base_files/icon/config.json", "rt", encoding="utf-8") as config_file:
    full_config = json.loads(config_file.read())
with open("../../games/umvc3/base_files/config.json", "rt", encoding="utf-8") as config_file:
    main_config = json.loads(config_file.read())

rescaling_factor = {}
for character_name in main_config["character_to_codename"].keys():
    codename = main_config["character_to_codename"][character_name]["codename"]
    current_character_rescaling_factor = {}

    for i in range(100):
        image_filename = f"../../games/umvc3/base_files/icon/{full_config['prefix']}{codename}{full_config['postfix']}{i:02}.png"
        if os.path.isfile(image_filename):
            image = Image.open(image_filename, "r").convert("RGBA")
            height = image.height

            current_costume_rescaling_factor = 1024.0/height
            current_character_rescaling_factor[f"{i}"] = current_costume_rescaling_factor

            print(codename, i, current_costume_rescaling_factor)
        else:
            print(f"Could not find {image_filename}")
    if current_character_rescaling_factor:
        rescaling_factor[codename] = deepcopy(current_character_rescaling_factor)
full_config["rescaling_factor"] = rescaling_factor
with open("../../games/umvc3/base_files/icon/config.json", "wt", encoding="utf-8") as config_file:
    config_file.write(json.dumps(full_config, indent=2))
