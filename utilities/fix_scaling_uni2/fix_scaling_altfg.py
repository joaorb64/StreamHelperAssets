from PIL import Image
from glob import glob
import json
import os.path

# file_list = glob("../../games/altfg/base_files/icon/*.png", recursive=True)
with open("../../games/altfg/base_files/icon/config.json", "rt", encoding="utf-8") as config_file:
    full_config = json.loads(config_file.read())
with open("../../games/altfg/base_files/config.json", "rt", encoding="utf-8") as config_file:
    main_config = json.loads(config_file.read())
with open("../../games/altfg/support/config.json", "rt", encoding="utf-8") as config_file:
    support_config = json.loads(config_file.read())

rescaling_factor = {}
support_rescaling_factor = {}
for character_name in main_config["character_to_codename"].keys():
    codename = main_config["character_to_codename"][character_name]["codename"]

    rescaling_factor[codename] = {}
    support_rescaling_factor[codename] = {}

    for i in range(5):
        image_filename = f"../../games/altfg/base_files/icon/{full_config['prefix']}{codename}{full_config['postfix']}{i:01}.png"
        if os.path.isfile(image_filename):
            image = Image.open(image_filename, "r").convert("RGBA")
            height = image.height
            rescaling_factor[codename][str(i)] = 256.0/height
            print(codename, rescaling_factor[codename][str(i)])
        else:
            print(f"Could not find {image_filename}")

        image_filename = f"../../games/altfg/support/{support_config['prefix']}{codename}{support_config['postfix']}{i:01}.png"
        if os.path.isfile(image_filename):
            image = Image.open(image_filename, "r").convert("RGBA")
            height = image.height
            support_rescaling_factor[codename][str(i)] = 250.0/height
            print(codename, support_rescaling_factor[codename][str(i)])
        else:
            print(f"Could not find {image_filename}")
        
full_config["rescaling_factor"] = rescaling_factor
support_config["rescaling_factor"] = support_rescaling_factor
with open("../../games/altfg/base_files/icon/config.json", "wt", encoding="utf-8") as config_file:
    config_file.write(json.dumps(full_config, indent=2))
with open("../../games/altfg/support/config.json", "wt", encoding="utf-8") as config_file:
    config_file.write(json.dumps(support_config, indent=2))
