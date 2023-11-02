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
        characters = config_file_content.get("character_to_codename").keys()
        nb_asset_packs_for_game = len(os.listdir(f"{path_to_games}/{dirname}"))
        list_games[dirname] = {
            "name": config_file_content.get("name"),
            "nb_asset_packs": nb_asset_packs_for_game,
            "nb_characters": len(characters)
        }
        with open(f"{characters_dir_name}/{''.join(x for x in config_file_content.get('name') if x.isalnum())}.txt", "wt", encoding='utf-8') as character_list_file:
            for character in characters:
                character_list_file.write(f"{character}\n")

list_games = {k: v for k, v in sorted(list_games.items(), key=lambda item: item[1]["name"].lower())}
character_total = 0
pkmn_total = 0

with open(f"./list_games.txt", 'wt', encoding='utf-8') as list_file:
    for game in list_games:
        has_s = ''
        game_name = list_games.get(game).get('name')
        nb_asset_packs_for_game = list_games.get(game).get("nb_asset_packs")
        nb_characters = list_games.get(game).get("nb_characters")
        if nb_asset_packs_for_game > 1:
            has_s = 's'
        if nb_characters > 1:
            char_has_s = 's'
        list_file.write(f"- {game_name} ({nb_asset_packs_for_game} asset pack{has_s}, {nb_characters} character{char_has_s})\n")
        if game != "pkmn":
            character_total += nb_characters
        else:
            pkmn_total += nb_characters

print("Number of games found:", len(list_games))
print("Number of characters found (Excuding Pokémon):", character_total)
print("Number of Pokémon found:", pkmn_total)
