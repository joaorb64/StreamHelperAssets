from PIL import Image
from glob import glob
import json
import os.path

# file_list = glob("../../games/pplanet/full/*.png", recursive=True)
with open("../../games/pplanet/full/config.json", "rt", encoding="utf-8") as config_file:
    full_config = json.loads(config_file.read())
with open("../../games/pplanet/base_files/config.json", "rt", encoding="utf-8") as config_file:
    main_config = json.loads(config_file.read())

rescaling_factor = {}
for character_name in main_config["character_to_codename"].keys():
    codename = main_config["character_to_codename"][character_name]["codename"]
    image_filename = f"../../games/pplanet/full/{full_config['prefix']}{codename}{full_config['postfix']}0.png"
    if os.path.isfile(image_filename):
        image = Image.open(image_filename, "r").convert("RGBA")
        height = image.height
        rescaling_factor[codename] = {"0": 2500.0/height}
        print(codename, rescaling_factor[codename]["0"])
    else:
        print(f"Could not find {image_filename}")
full_config["rescaling_factor"] = rescaling_factor
with open("../../games/pplanet/full/config.json", "wt", encoding="utf-8") as config_file:
    config_file.write(json.dumps(full_config, indent=2))
