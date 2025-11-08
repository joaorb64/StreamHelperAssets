import json
from copy import deepcopy
from glob import glob

# Define the base directory
base_dir = './games/'
list_csv = glob(f"./scripts/csv/*.csv")
for path in list_csv:
    game = path.split("/")[-1].replace(".csv", "")
    config_path = f"{base_dir}{game}/base_files/config.json"
    csv_path = f"./scripts/csv/{game}.csv"

    with open(config_path, "rt", encoding="utf-8") as config_file:
        config_json = json.loads(config_file.read())

    with open(csv_path, "rt", encoding="utf-8") as csv_file:
        csv_lines = csv_file.readlines()
        header_line = csv_lines[0].strip().split(",")
        data = csv_lines[1:]
        for i in range(1, len(header_line)):
            print(header_line[i])
            for data_line in data:
                if "pkmn.csv" not in path:
                    character_data = config_json["character_to_codename"][header_line[i]]
                    character_name = header_line[i]
                else:
                    for character_name in config_json["character_to_codename"].keys():
                        if int(config_json["character_to_codename"][character_name].get("codename")) == int(header_line[i]):
                            character_data = config_json["character_to_codename"][character_name]
                            break
                skin_data = character_data.get("skin_name")
                skin_names = data_line.strip().split(",")
                skin_name = skin_names[i]
                print(skin_name)
                if skin_name:
                    if not skin_data:
                        character_data["skin_name"] = {}
                    if character_data["skin_name"].get(skin_names[0]):
                        character_data["skin_name"][skin_names[0]]["name"] = skin_name
                    else:
                        character_data["skin_name"][skin_names[0]] = {"name": skin_name}
                config_json["character_to_codename"][character_name] = character_data

    with open(config_path, "wt", encoding="utf-8") as config_file:
        config_file.write(json.dumps(config_json, indent=2))