import json
from pathlib import Path

mappings = {}

with open("TSH_API_Mappings.csv", 'rt', encoding="utf-8") as source_file:
    lines = source_file.readlines()
    for line in lines:
        if line.strip():
            line_split = line.strip().split(",")
            if line_split[0] != "codename":
                mappings[line_split[0]] = {
                    "igdb_game_id": line_split[1],
                    "steamgriddb_game_id": line_split[2]
                }
                if mappings[line_split[0]].get("steamgriddb_game_id"):
                    mappings[line_split[0]]["steamgriddb_game_id"] = int(mappings[line_split[0]]["steamgriddb_game_id"])
                else:
                    mappings[line_split[0]]["steamgriddb_game_id"] = None

all_games_path = "../../games"

for codename in mappings.keys():
    game_path = f"{all_games_path}/{codename}/base_files/config.json"
    if Path(game_path).is_file:
        with open(game_path, 'rt', encoding="utf-8") as game_file:
            game_json = json.loads(game_file.read())
        for id_key in ["igdb_game_id", "steamgriddb_game_id"]:
            if mappings[codename].get(id_key):
                game_json[id_key] = mappings[codename][id_key]
        with open(game_path, 'wt', encoding="utf-8") as game_file:
            game_file.write(json.dumps(game_json, indent=2))
