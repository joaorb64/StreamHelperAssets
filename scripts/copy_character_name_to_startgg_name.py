import json

base_dir = './games/'
game = "punite"

with open(f"{base_dir}{game}/base_files/config.json", "rt", encoding="utf-8") as config_file:
    config_json = json.loads(config_file.read())

for character_name in config_json["character_to_codename"].keys():
    config_json["character_to_codename"][character_name]["smashgg_name"] = character_name

with open(f"{base_dir}{game}/base_files/config.json", "wt", encoding="utf-8") as config_file:
    config_file.write(json.dumps(config_json, indent=2))
