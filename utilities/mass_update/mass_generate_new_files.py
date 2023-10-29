import json
import os

game_codename = "bh"

config_path = f"../../games/{game_codename}/base_files/config.json"
asset_pack = "full"
asset_config_path = f"../../games/{game_codename}/{asset_pack}/config.json"

with open(config_path, "rt", encoding="utf-8") as config_file:
    config = json.loads(config_file.read())

with open(asset_config_path, "rt", encoding="utf-8") as asset_config_file:
    asset_config = json.loads(asset_config_file.read())

characters = config.get("character_to_codename")

eyesights_dict = {}
new_file_list = []

for character_name in characters.keys():
    codename = characters[character_name].get("codename")
    prefix = asset_config.get("prefix")
    postfix = asset_config.get("postfix")
    file_path = f"../../games/{game_codename}/{asset_pack}/{prefix}{codename}{postfix}0.png"
    if not os.path.exists(file_path):
        new_file_list.append(f"{file_path}")
    if codename not in asset_config.get("eyesights").keys():
        eyesights_dict[codename] = {0: {"x": 0, "y": 0}}

with open("eyesights.json", "wt", encoding="utf-8") as eyesights_file:
    eyesights_file.write(json.dumps({"eyesights": eyesights_dict}, indent=2))

for file_path in new_file_list:
    with open(file_path, "wb") as new_file:
        new_file.write(bytearray())
