from PIL import Image
from glob import glob
import json

# file_list = glob("../../games/ostrikers/art/*.png", recursive=True)
with open("../../games/ostrikers/art/config.json", "rt", encoding="utf-8") as config_file:
    art_config = json.loads(config_file.read())
with open("../../games/ostrikers/base_files/config.json", "rt", encoding="utf-8") as config_file:
    main_config = json.loads(config_file.read())

rescaling_factor = {}
for character_name in main_config["character_to_codename"].keys():
    codename = main_config["character_to_codename"][character_name]["codename"]
    image_filename = f"../../games/ostrikers/art/{art_config['prefix']}{codename}{art_config['postfix']}0.png"
    image = Image.open(image_filename, "r").convert("RGBA")
    height = image.height
    rescaling_factor[codename] = {"0": 5000.0/height}
    print(codename, rescaling_factor[codename]["0"])
art_config["rescaling_factor"] = rescaling_factor
with open("../../games/ostrikers/art/config.json", "wt", encoding="utf-8") as config_file:
    config_file.write(json.dumps(art_config, indent=2))
