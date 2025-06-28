from pathlib import Path
from glob import glob
import json
import shutil

source_folder = "source/Game/Chara"
out_folder = "out"
shutil.rmtree(out_folder)
Path.mkdir(out_folder, exist_ok=True)

with open("chara.json", "rt", encoding="utf-8") as file:
    list_index = json.loads(file.read())

for index in list_index.keys():
    source_chara_folder = f"{source_folder}/{index}"
    codename = list_index[index]
    i = 0
    filename_base = f"{out_folder}/file_1.1_{codename}_"

    # Parse base costumes
    base_costumes_folder = f"{source_chara_folder}/UI_N/ChaSelect/1P"
    list_textures = list(glob(f"{base_costumes_folder}/*.png"))
    list_textures.sort()
    for texture in list_textures:
        shutil.copyfile(texture, f"{filename_base}{i:02}.png")
        i += 1
    
    # Parse alt costumes
    list_textures = list(glob(f"{source_chara_folder}/UI_AR*/ChaSelect/1P/*.png"))
    list_textures.sort()
    for texture in list_textures:
        shutil.copyfile(texture, f"{filename_base}{i:02}.png")
        i += 1
