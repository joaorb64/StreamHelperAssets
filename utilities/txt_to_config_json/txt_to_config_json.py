import json
import requests
from pathlib import Path

game_id = 5690
character_list_filename = "characters_list.txt"

with open(f"../download_smashgg/game_data.json", 'rt') as game_data_file:
    game_data = json.loads(game_data_file.read())
found = False
for game in game_data:
    if game.get("smashgg_id") == game_id:
        game_name = game.get("name")
        image_type = game.get("image_type")
        found = True

if not found:
    print("Game not found")
    exit(1)

with open(f"config.json", 'wt') as config_file:
    description = "Base config to use this game."
    credits = ''
    version = "1.0"

    config_dict: dict = {
        "name": str(game_name),
        "smashgg_game_id": game_id,
        "character_to_codename": {},
        "stage_to_codename": {},
        "version": version,
        "description": str(description),
        "credits": str(credits)
    }

    with open(f"{character_list_filename}", 'r') as character_list:
        for character_name in character_list:
            character_name = character_name.replace('\n', '')
            if character_name:
                codename = character_name.replace(' ', '').replace('&', '').replace(
                    '.', '').replace('(', '').replace(')', '').replace('-', '')
                config_dict["character_to_codename"][character_name] = {
                    "codename": codename
                }

    config_file_content = json.dumps(config_dict, indent=2)
    config_file.write(config_file_content)
