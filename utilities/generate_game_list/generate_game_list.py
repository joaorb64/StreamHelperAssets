import os
import json

list_games = {}


path_to_games = "../../games"

for dirname in os.listdir(path_to_games):
    with open(f"{path_to_games}/{dirname}/base_files/config.json", 'rt', encoding='utf-8') as config_file:
        config_file_content = json.load(config_file)
        nb_asset_packs_for_game = len(os.listdir(f"{path_to_games}/{dirname}"))
        list_games[dirname] = {
            "name": config_file_content.get("name"),
            "nb_asset_packs": nb_asset_packs_for_game
        }

with open(f"./list_games.txt", 'wt', encoding='utf-8') as list_file:
    for game in list_games:
        has_s = ''
        game_name = list_games.get(game).get('name')
        nb_asset_packs_for_game = list_games.get(game).get("nb_asset_packs")
        if nb_asset_packs_for_game > 1:
            has_s = 's'
        list_file.write(f"- {game_name} ({nb_asset_packs_for_game} asset pack{has_s})\n")

print("Number of games found:", len(list_games))
