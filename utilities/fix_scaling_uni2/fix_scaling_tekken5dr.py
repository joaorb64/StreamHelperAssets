from PIL import Image
from glob import glob
import json
import os.path

# file_list = glob("../../games/tekken5dr/base_files/icon/*.png", recursive=True)
with open("../../games/tekken5dr/base_files/icon/config.json", "rt", encoding="utf-8") as config_file:
    icon_config = json.loads(config_file.read())
with open("../../games/tekken5dr/full/config.json", "rt", encoding="utf-8") as config_file:
    full_config = json.loads(config_file.read())
with open("../../games/tekken5dr/base_files/config.json", "rt", encoding="utf-8") as config_file:
    main_config = json.loads(config_file.read())

full_rescaling_factor = {}
for character_name in main_config["character_to_codename"].keys():
    codename = main_config["character_to_codename"][character_name]["codename"]

    full_rescaling_factor[codename] = {}

    for i in range(5):
        image_filename = f"../../games/tekken5dr/full/{full_config['prefix']}{codename}{full_config['postfix']}{i:01}.png"
        if os.path.isfile(image_filename):
            image = Image.open(image_filename, "r").convert("RGBA")
            height = image.height
            full_rescaling_factor[codename][str(i)] = 720.0/height
            print(codename, full_rescaling_factor[codename][str(i)])
        else:
            print(f"Could not find {image_filename}")
        
full_config["rescaling_factor"] = full_rescaling_factor
with open("../../games/tekken5dr/full/config.json", "wt", encoding="utf-8") as config_file:
    config_file.write(json.dumps(full_config, indent=2))
