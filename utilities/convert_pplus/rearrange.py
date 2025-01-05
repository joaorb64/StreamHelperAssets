import json
import os
import glob
from copy import deepcopy
import shutil

base_dir = "../../games/pplus"

with open(f"{base_dir}/base_files/config.json", "rt", encoding="utf-8") as main_config_file:
    main_config = json.loads(main_config_file.read())

top8er_names = {}
for character_name in main_config.get("character_to_codename"):
    if character_name not in ["Random", "Giga Bowser", "Wario-Man"]:
        top8er_names[character_name] = character_name.replace(" ", "_").replace("&", "_")
        if character_name == "R.O.B.":
            top8er_names[character_name] = "ROB"

main_config_new_tsh = deepcopy(main_config)

for character_name in top8er_names:
    tsh_codename = main_config.get("character_to_codename")[character_name]["codename"]
    top8er_name = top8er_names[character_name]
    os.rename(f"{base_dir}/base_files/icon_hd/{top8er_name}-0.png", f"{base_dir}/base_files/icon_hd/icon_hd_{tsh_codename}_000.png")

    costumes_files = glob.glob(f"{base_dir}/portrait_hd/{top8er_name}-*.png")
    skin_data = {}
    index = 0
    for costume_file_path in costumes_files:
        costume_file_name = os.path.basename(costume_file_path)
        costume_name = costume_file_name.replace(".png", "").split("-")[-1]
        if not costume_name.isdigit():
            skin_data[str(index)] = {
                "name": costume_name
            }
        os.rename(costume_file_path, f"{base_dir}/portrait_hd/portrait_hd_{tsh_codename}_{index:04}.png")
        index +=1
    main_config_new_tsh["character_to_codename"][character_name]["skin_name"] = skin_data

with open(f"{base_dir}/base_files/config_new.json", "wt", encoding="utf-8") as main_config_file_new_tsh:
    main_config_file_new_tsh.write(json.dumps(main_config_new_tsh, indent=2))

icon_config = {
  "prefix": "icon_hd_",
  "postfix": "_",
  "type": [
    "icon"
  ],
  "version": "1.0"
}

portrait_config = {"name": "Portraits",
  "description": "Character portraits as seen on the Character Select Screen",
  "prefix": "portrait_hd_",
  "postfix": "_",
  "type": [
    "portrait"
  ],
  "credits": "",
  "version": "1.0"
}

with open(f"{base_dir}/base_files/icon_hd/config.json", "wt", encoding="utf-8") as icon_config_file:
    icon_config_file.write(json.dumps(icon_config, indent=2))

with open(f"{base_dir}/portrait_hd/config.json", "wt", encoding="utf-8") as portrait_config_file:
    portrait_config_file.write(json.dumps(portrait_config, indent=2))

shutil.rmtree(f"{base_dir}/portrait")
shutil.rmtree(f"{base_dir}/base_files/icon")

os.rename(f"{base_dir}/portrait_hd", f"{base_dir}/portrait")
os.rename(f"{base_dir}/base_files/icon_hd", f"{base_dir}/base_files/icon")