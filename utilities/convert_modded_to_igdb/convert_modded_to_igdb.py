import os
import json
from pathlib import Path

characters_dir_name = "characters"
Path(characters_dir_name).mkdir(parents=True, exist_ok=True)

list_games = {}


path_to_games = "../../games"

for dirname in os.listdir(path_to_games):
    with open(f"{path_to_games}/{dirname}/base_files/config.json", 'rt', encoding='utf-8') as config_file:
        config_file_content = json.load(config_file)

    igdb_alt_game_list = []
    for alt_game in config_file_content.get("alternate_versions", []):
        if alt_game.get("igdb_game_id"):
            igdb_alt_game_list.append(alt_game.get("igdb_game_id"))

    content_sections_list = ["character_to_codename", "variant_to_codename", "stage_to_codename"]

    for content_section in content_sections_list:
        for content_key in config_file_content.get(content_section, {}).keys():
            is_modded = config_file_content.get(content_section, {}).get(content_key).get("modded")
            if is_modded and igdb_alt_game_list:
                config_file_content[content_section][content_key]["igdb_playable_list"] = igdb_alt_game_list

    with open(f"{path_to_games}/{dirname}/base_files/config.json", 'wt', encoding='utf-8') as config_file:
        config_file.write(json.dumps(config_file_content, indent=2))