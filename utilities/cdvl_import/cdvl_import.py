import json
import shutil
import glob

list_character_path = glob.glob("./input/*/")
list_characters = []
for i in range(len(list_character_path)):
    list_characters.append(list_character_path[i].split("/")[-2])

icon_path = "../../games/cdvl/base_files/icon"
full_path = "../../games/cdvl/full"

for i in range(len(list_character_path)):
    character = list_characters[i]
    character_path = list_character_path[i]

    skin_data = {}

    image_paths = sorted(glob.glob(f"{character_path}*.png"))
    print(image_paths)
    
    icon_index = 0
    full_index = 0

    for image_path in image_paths:
        image_name = image_path.split("/")[-1]
        if image_name.startswith("Avatar"):
            if not skin_data.get(icon_index):
                skin_data[icon_index] = {}
            skin_data[icon_index]["icon"] = image_path
            icon_index += 1

        if image_name.startswith("Portrait"):
            if not skin_data.get(full_index):
                skin_data[full_index] = {}
            skin_data[full_index]["full"] = image_path
            full_index += 1
    
    for index in skin_data.keys():
        new_icon_path = f"{icon_path}/file_{character}_{index:02}.png"
        new_full_path = f"{full_path}/file_{character}_{index:02}.png"
    
        if skin_data[index].get("icon"):
            shutil.move(skin_data[index]["icon"], new_icon_path)
        
        if skin_data[index].get("full"):
            shutil.move(skin_data[index]["full"], new_full_path)
