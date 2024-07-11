from pathlib import Path
from PIL import Image
from glob import glob
import json
import os

game = "mk1"
pack = "portrait"

dir_path = f"../../games/{game}/{pack}"
png_path_list = glob(f"{dir_path}/*.png")
config_path = f"{dir_path}/config.json"

with open(config_path, 'rt', encoding='utf-8')as config_file:
    config = json.loads(config_file.read())
    prefix = config.get("prefix")
    postfix = config.get("postfix")
    eyesights = config.get("eyesights", {})

for png_path in png_path_list:
    file_name = os.path.basename(png_path)
    print(file_name)
    image = Image.open(png_path).convert("RGBA")
    image = image.transpose(Image.FLIP_LEFT_RIGHT)
    
    current_codename = None
    current_skin = None
    for codename in eyesights.keys():
        if file_name.startswith(f"{prefix}{codename}{postfix}"):
            current_codename = codename
            current_skin = file_name.replace(f"{prefix}{codename}{postfix}", "").replace(".png", "")
    if current_codename:
        config["eyesights"][current_codename][current_skin]["x"] = image.width - config["eyesights"][current_codename][current_skin]["x"]
    
    image.save(png_path)

description_addon = "Flipped for use with TSH’s default settings"
if config.get("description"):
    config["description"] = config["description"] + "\n" + description_addon
else:
    config["description"] = description_addon

with open(config_path, "wt", encoding="utf-8") as config_file:
    config_file.write(json.dumps(config, indent=2))
