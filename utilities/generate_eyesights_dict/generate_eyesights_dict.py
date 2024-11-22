import json
import collections

game_codename = "smk"

config_path = f"../../games/{game_codename}/base_files/config.json"

with open(config_path, "rt", encoding="utf-8") as config_file:
    config = json.loads(config_file.read())

characters = config.get("character_to_codename")

eyesights_dict = {}

for character_name in characters.keys():
    eyesights_dict[characters[character_name].get("codename")] = {0: {"x": 0, "y": 0}}

eyesights_dict = collections.OrderedDict(sorted(eyesights_dict.items()))

with open("eyesights.json", "wt", encoding="utf-8") as eyesights_file:
    eyesights_file.write(json.dumps({"eyesights": eyesights_dict}, indent=2))
