import json
import collections

game_codename = "sf6"

config_path = f"../../games/{game_codename}/base_files/config.json"

with open(config_path, "rt", encoding="utf-8") as config_file:
    config = json.loads(config_file.read())

characters = config.get("character_to_codename")

url_dict = {}

for character_name in characters.keys():
    url_dict[characters[character_name].get("codename")] = {"url": ""}

url_dict = collections.OrderedDict(sorted(url_dict.items()))

with open("sound.json", "wt", encoding="utf-8") as eyesights_file:
    eyesights_file.write(json.dumps({"sound": url_dict}, indent=2))
