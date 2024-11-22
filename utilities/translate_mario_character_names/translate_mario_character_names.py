import requests
import json
from copy import deepcopy

list_games_to_translate = ["sms", "msc", "msbl", "mkwii", "mk64", "mk8dx", "msb", "mta", "ssb64", "ssbm", "ssbb", "ssbu", "ssbwiiu", "smk"]
exclude_locale = ["en_US"]
convert_locale = {"SC": "zh_CN", "TC": "zh_TW", "fr_FR": "fr",
                  "de_DE": "de", "it_IT": "it", "nl_NL": "nl", "ru_RU": "ru", "ko_KR": "ko", "ja_JP": "ja", "es_ES": "es"}

with open("./source.json", 'rt', encoding='utf-8') as fighter_database_file:
    fighter_database_text = fighter_database_file.read()
    fighter_database = json.loads(fighter_database_text)

for game in list_games_to_translate:
    print(game)
    config_file_path = f"../../games/{game}/base_files/config.json"
    with open(config_file_path, 'rt', encoding="utf-8") as config_file:
        txt_contents = config_file.read()
        config_file_json = json.loads(txt_contents)
    config_character_dict = deepcopy(config_file_json["character_to_codename"])
    for character in config_character_dict.keys():
        for data in fighter_database["fighters"]:
            if data["displayName"]["en_US"].upper().replace("<BR>& ", "& ") == character.upper():
                if not config_character_dict[character].get("locale"):
                    config_character_dict[character]["locale"] = {}
                for locale in data["displayName"].keys():
                    if locale not in exclude_locale:
                        actual_locale = locale
                        if convert_locale.get(locale):
                            actual_locale = convert_locale.get(locale)
                        if actual_locale not in config_character_dict[character]["locale"].keys():
                            config_character_dict[character]["locale"][actual_locale] = data["displayName"][locale]
                break
    config_file_json["character_to_codename"] = config_character_dict
    with open(config_file_path, 'wt', encoding="utf-8") as config_file:
        txt_contents = json.dumps(config_file_json, indent=2)
        config_file.write(txt_contents)
