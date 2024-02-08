from PIL import Image
from glob import glob
import json

# file_list = glob("../../games/uni2/full/*.png", recursive=True)
with open("../../games/uni2/full/config.json", "rt", encoding="utf-8") as config_file:
    full_config = json.loads(config_file.read())
with open("../../games/uni2/base_files/config.json", "rt", encoding="utf-8") as config_file:
    main_config = json.loads(config_file.read())

rescaling_factor = {}
for character_name in main_config["character_to_codename"].keys():
    codename = main_config["character_to_codename"][character_name]["codename"]
    image_filename = f"../../games/uni2/full/{full_config['prefix']}{codename}{full_config['postfix']}0.png"
    image = Image.open(image_filename, "r").convert("RGBA")
    height = image.height
    rescaling_factor[codename] = {"0": 2000.0/height}
    print(codename, rescaling_factor[codename]["0"])
full_config["rescaling_factor"] = rescaling_factor
with open("../../games/uni2/full/config.json", "wt", encoding="utf-8") as config_file:
    config_file.write(json.dumps(full_config, indent=2))
