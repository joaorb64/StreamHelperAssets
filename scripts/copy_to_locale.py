import json

to_copy = [
    # "character", 
    "stage",
    # "variant"
    ]  # Can be character, stage or variant
languages = ["fr"]
games = ["kar2"]

for game in games:
    config_path = f"./games/{game}/base_files/config.json"
    with open(config_path, "rt", encoding="utf-8") as config_file:
        config = json.loads(config_file.read())
    
    for data_type in to_copy:
        for data_key in config.get(f"{data_type}_to_codename", {}).keys():
            if "locale" not in config.get(f"{data_type}_to_codename", {}).get(data_key, {}).keys():
                config[f"{data_type}_to_codename"][data_key]["locale"] = {}
            for locale in languages:
                config[f"{data_type}_to_codename"][data_key]["locale"][locale] = data_key

    with open(config_path, "wt", encoding="utf-8") as config_file:
        config_file.write(json.dumps(config, indent=2))
