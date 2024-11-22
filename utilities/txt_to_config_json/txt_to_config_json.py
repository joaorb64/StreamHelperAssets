import json
from pathlib import Path

game_id = 5711
character_list_filename = "characters_list.txt"

blank_files_folder="blank_files"
Path(blank_files_folder).mkdir(parents=True, exist_ok=True)

with open(f"../download_smashgg/game_data.json", 'rt', encoding="utf-8") as game_data_file:
    game_data = json.loads(game_data_file.read())
found = False
for game in game_data:
    if game.get("smashgg_id") == game_id:
        game_name = game.get("name")
        image_type = game.get("image_type")
        challonge_id = game.get("challonge_id")
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
        "challonge_game_id": challonge_id,
        "character_to_codename": {},
        "stage_to_codename": {},
        "version": version,
        "description": str(description),
        "credits": str(credits)
    }

    with open(f"{character_list_filename}", 'rt', encoding='utf-8') as character_list:
        for character_name in character_list:
            character_name = character_name.strip()
            if character_name:
                codename = character_name
                for str_character in " &.()?!;/:%\\|-_\"'~@[{}]":
                    codename = codename.replace(str_character, "")
                config_dict["character_to_codename"][character_name] = {
                    "codename": codename
                }
                with open(f"{blank_files_folder}/file_{codename}_0.png", "wb") as blank_character_file:
                    blank_character_file.write(bytearray())

    config_file_content = json.dumps(config_dict, indent=2, sort_keys=True)
    config_file.write(config_file_content)
