import json
from copy import deepcopy

# Main weapons

file_path = "../../games/spl3/base_files/config.json"
with open(file_path, 'rt', encoding='utf-8') as config_file:
    config_dict = json.loads(config_file.read())

new_file_path = "./spl3/base_files/config.json"
with open(new_file_path, 'rt', encoding='utf-8') as new_config_file:
    new_config_dict = json.loads(new_config_file.read())

config_dict["version"] = new_config_dict["version"]
config_dict["stage_to_codename"] = new_config_dict["stage_to_codename"]

for weapon in new_config_dict["character_to_codename"].keys():
    if weapon not in config_dict["character_to_codename"].keys():
        config_dict["character_to_codename"][weapon] = new_config_dict["character_to_codename"][weapon]

with open(new_file_path, 'wt', encoding='utf-8') as new_config_file:
    new_config_file.write(json.dumps(config_dict, indent=2))


# Side weapons

folder_keys = ["sub", "special"]
for folder_key in folder_keys:
    file_path = f"../../games/spl3/{folder_key}/config.json"
    with open(file_path, 'rt', encoding='utf-8') as config_file:
        config_dict = json.loads(config_file.read())

    new_file_path = f"./spl3/{folder_key}/config.json"
    with open(new_file_path, 'rt', encoding='utf-8') as new_config_file:
        new_config_dict = json.loads(new_config_file.read())

    config_dict["version"] = new_config_dict["version"]

    for weapon in new_config_dict["metadata"][0]["values"].keys():
        if weapon not in config_dict["metadata"][0]["values"].keys():
            secondary_name = new_config_dict["metadata"][0]["values"][weapon]["value"]
            secondary_found = False
            for old_weapon in deepcopy(config_dict["metadata"][0]["values"]).keys():
                if config_dict["metadata"][0]["values"][old_weapon]["value"] == secondary_name:
                    config_dict["metadata"][0]["values"][weapon] = {
                        "value" : secondary_name,
                        "locale": config_dict["metadata"][0]["values"][old_weapon]["locale"]
                    }
                    secondary_found = True
            if not secondary_found:
                config_dict["metadata"][0]["values"][weapon] = new_config_dict["metadata"][0]["values"][weapon]

    with open(new_file_path, 'wt', encoding='utf-8') as new_config_file:
        new_config_file.write(json.dumps(config_dict, indent=2))