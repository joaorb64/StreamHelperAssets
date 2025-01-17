import json
import os
import glob
from copy import deepcopy
import shutil
from PIL import Image

base_dir = "../../games/pplus"

images_path = glob.glob(f"{base_dir}/portrait/*.png")
base_image_file_path = f"{base_dir}/portrait/portrait_hd_00_0000.png"
base_image = Image.open(base_image_file_path)
base_height = base_image.height

config_path = f"{base_dir}/portrait/config.json"
with open(config_path, "rt", encoding="utf-8") as config_file:
    config = json.loads(config_file.read())
    og_eyesights = config.get("eyesights")

new_eyesights = {}
new_scaling = {}

for image_path in images_path:
    image_name = os.path.basename(image_path)
    directory_name = os.path.dirname(image_path)
    codename = image_name.split("_")[-2]
    index = str(int(image_name.split("_")[-1].split(".")[0]))
    image = Image.open(image_path)
    scaling = base_height/image.height
    skin_0_path = f"{directory_name}/portrait_hd_{codename}_0000.png"
    skin_0 = Image.open(skin_0_path)
    scaling_to_skin_0 = skin_0.height/image.height
    if codename not in new_eyesights.keys() and codename in og_eyesights:
        new_eyesights[codename] = {}
    if codename not in new_scaling:
        new_scaling[codename] = {}
    if index in og_eyesights.get(codename, {}).keys():
        old_eyesight = og_eyesights.get(codename, {}).get(index)
        new_eyesight = old_eyesight
    elif "0" in og_eyesights.get(codename, {}).keys():
        old_eyesight = og_eyesights.get(codename, {}).get("0")
        new_eyesight = {
            "x": int(old_eyesight["x"]/scaling_to_skin_0),
            "y": int(old_eyesight["y"]/scaling_to_skin_0)
        }
    else:
        old_eyesight = None
        new_eyesight = None
    if new_eyesight:
        if int(index) == 0 or new_eyesight != new_eyesights.get(codename, {}).get("0"):
            new_eyesights[codename][index] = new_eyesight
    if int(index) == 0 or scaling != new_scaling.get(codename, {}).get("0", 1.0):
        new_scaling[codename][index] = scaling
    print(image.height*scaling)

config["eyesights"] = new_eyesights
config["rescaling_factor"] = new_scaling

with open(config_path, "wt", encoding="utf-8") as config_file:
    config_file.write(json.dumps(config, indent=2))
