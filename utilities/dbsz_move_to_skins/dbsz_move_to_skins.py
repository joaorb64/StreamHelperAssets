import json
import os
from copy import deepcopy

root_path = "../../games/dbsz"
base_files_path = f"{root_path}/base_files"
config_path = f"{base_files_path}/config.json"
icon_path = f"{base_files_path}/icon"
icon_config_path = f"{icon_path}/config.json"

with open(config_path, 'rt', encoding="utf-8") as config_file:
    config_dict = json.loads(config_file.read())

with open(icon_config_path, 'rt', encoding="utf-8") as icon_config_file:
    icon_config_dict = json.loads(icon_config_file.read())

character_list = config_dict["character_to_codename"]
new_character_list = {}
converter = {}
eyesights_dict = icon_config_dict["eyesights"]
new_eyesights_dict = {}
for character_name in character_list.keys():
    original_filename = f'{icon_path}/{icon_config_dict["prefix"]}{character_list[character_name]["codename"]}{icon_config_dict["postfix"]}0.jpg'
    # print(original_filename)
    parse = character_name.split(" - ")
    new_character_name = parse[0]
    if len(parse) > 1:
        form_name = parse[1]
    else:
        form_name = ""
    if new_character_name not in new_character_list.keys():
        converter[new_character_name] = [character_name]
        new_character_list[new_character_name] = {
            "codename": character_list[character_name]["codename"]
        }
        if form_name:
            new_character_list[new_character_name]["skin_name"] = {"0": {"name": form_name}}
        else:
            new_character_list[new_character_name]["skin_name"] = {}
        new_eyesights_dict[character_list[character_name]["codename"]] = {
            "0": eyesights_dict[character_list[character_name]["codename"]]["0"]
        }
        new_filename = f'{icon_path}/{icon_config_dict["prefix"]}{character_list[character_name]["codename"]}{icon_config_dict["postfix"]}0.jpg'
    else:
        converter[new_character_name].append(character_name)
        skin_number = str(len(converter[new_character_name])-1)
        if form_name:
            new_character_list[new_character_name]["skin_name"][skin_number] = {"name": form_name}
        new_eyesights_dict[new_character_list[new_character_name]["codename"]][skin_number] = eyesights_dict[character_list[character_name]["codename"]]["0"]
        new_filename = f'{icon_path}/{icon_config_dict["prefix"]}{new_character_list[new_character_name]["codename"]}{icon_config_dict["postfix"]}{skin_number}.jpg'
    # print(new_filename)
    if original_filename != new_filename:
        os.rename(original_filename, new_filename)


config_dict["character_to_codename"] = new_character_list
icon_config_dict["eyesights"] = new_eyesights_dict

with open(config_path, 'wt', encoding="utf-8") as config_file:
    config_file.write(json.dumps(config_dict, indent=2))
    
with open(icon_config_path, 'wt', encoding="utf-8") as icon_config_file:
    icon_config_file.write(json.dumps(icon_config_dict, indent=2))
