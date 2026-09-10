from PIL import Image
from glob import glob
import json
import os.path

# file_list = glob("../../games/doa6/base_files/icon/*.png", recursive=True)
with open("../../games/doa6/base_files/icon/config.json", "rt", encoding="utf-8") as config_file:
    icon_config = json.loads(config_file.read())
with open("../../games/doa6/full/config.json", "rt", encoding="utf-8") as config_file:
    full_config = json.loads(config_file.read())
with open("../../games/doa6/base_files/config.json", "rt", encoding="utf-8") as config_file:
    main_config = json.loads(config_file.read())

icon_rescaling_factor = {}
full_rescaling_factor = {}
for character_name in main_config["character_to_codename"].keys():
    codename = main_config["character_to_codename"][character_name]["codename"]
    image_filename = f"../../games/doa6/base_files/icon/{icon_config['prefix']}{codename}{icon_config['postfix']}0.png"
    if os.path.isfile(image_filename):
        image = Image.open(image_filename, "r").convert("RGBA")
        height = image.height
        icon_rescaling_factor[codename] = {"0": 960.0/height}
        print(codename, icon_rescaling_factor[codename]["0"])
    else:
        print(f"Could not find {image_filename}")

    image_filename = f"../../games/doa6/full/{full_config['prefix']}{codename}{full_config['postfix']}0.png"
    if os.path.isfile(image_filename):
        image = Image.open(image_filename, "r").convert("RGBA")
        height = image.height
        full_rescaling_factor[codename] = {"0": 2000.0/height}
        print(codename, full_rescaling_factor[codename]["0"])
    else:
        print(f"Could not find {image_filename}")

icon_config["rescaling_factor"] = icon_rescaling_factor
full_config["rescaling_factor"] = full_rescaling_factor
with open("../../games/doa6/base_files/icon/config.json", "wt", encoding="utf-8") as config_file:
    config_file.write(json.dumps(icon_config, indent=2))
with open("../../games/doa6/full/config.json", "wt", encoding="utf-8") as config_file:
    config_file.write(json.dumps(full_config, indent=2))
