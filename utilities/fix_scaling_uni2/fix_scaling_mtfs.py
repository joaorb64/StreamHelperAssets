from PIL import Image
from glob import glob
import json
import os.path

with open("../../games/mtfs/full/config.json", "rt", encoding="utf-8") as config_file:
    full_config = json.loads(config_file.read())
with open("../../games/mtfs/base_files/config.json", "rt", encoding="utf-8") as config_file:
    main_config = json.loads(config_file.read())
with open("../../games/mtfs/stand/config.json", "rt", encoding="utf-8") as config_file:
    stand_config = json.loads(config_file.read())

stand_rescaling_factor = {}
full_rescaling_factor = {}
for character_name in main_config["character_to_codename"].keys():
    codename = main_config["character_to_codename"][character_name]["codename"]

    stand_rescaling_factor[codename] = {}
    full_rescaling_factor[codename] = {}

    for i in range(5):

        image_filename = f"../../games/altfg/stand/{stand_config['prefix']}{codename}{stand_config['postfix']}{i:01}.png"
        if os.path.isfile(image_filename):
            image = Image.open(image_filename, "r").convert("RGBA")
            height = image.height
            stand_rescaling_factor[codename][str(i)] = 4929.0/height
            print(codename, stand_rescaling_factor[codename][str(i)])
        else:
            print(f"Could not find {image_filename}")

        image_filename = f"../../games/altfg/full/{full_config['prefix']}{codename}{full_config['postfix']}{i:01}.png"
        if os.path.isfile(image_filename):
            image = Image.open(image_filename, "r").convert("RGBA")
            height = image.height
            full_rescaling_factor[codename][str(i)] = 4929.0/height
            print(codename, stand_rescaling_factor[codename][str(i)])
        else:
            print(f"Could not find {image_filename}")
        
stand_config["rescaling_factor"] = stand_rescaling_factor
full_config["rescaling_factor"] = full_rescaling_factor
with open("../../games/altfg/stand/config.json", "wt", encoding="utf-8") as config_file:
    config_file.write(json.dumps(stand_config, indent=2))
with open("../../games/altfg/full/config.json", "wt", encoding="utf-8") as config_file:
    config_file.write(json.dumps(full_config, indent=2))
