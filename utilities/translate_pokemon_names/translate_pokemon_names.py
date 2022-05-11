import requests
import json
from copy import deepcopy

link_to_names = "https://raw.githubusercontent.com/sindresorhus/pokemon/main/data/[lang].json"
lang_list = ["fr", "de", "ko", "ja", "zh-hans", "zh-hant"]
config_file_path = "../../games/pkmn/base_files/config.json"

with open(config_file_path, 'rt', encoding='utf-8') as config_file:
    config_contents_text = config_file.read()
    config_contents = json.loads(config_contents_text)

list_pokemon_by_lang = {}
for current_locale in lang_list:
    actual_locale = deepcopy(current_locale)
    if current_locale == "zh-hans":
        actual_locale = "zh_CN"
    if current_locale == "zh-hant":
        actual_locale = "zh_TW"
    response = requests.get(link_to_names.replace("[lang]", current_locale))
    list_of_pokemon = json.loads(response.text)
    list_pokemon_by_lang[actual_locale] = deepcopy(list_of_pokemon)
    
codenames_dict = config_contents.get("character_to_codename")
for character in codenames_dict.keys():
    print(character)
    codename = codenames_dict.get(character).get("codename")
    index = int(codename)-1
    if not codenames_dict.get(character).get("locale"):
        config_contents["character_to_codename"][character]["locale"] = {}
    for current_locale in list_pokemon_by_lang.keys():
        config_contents["character_to_codename"][character]["locale"][current_locale] = list_pokemon_by_lang[current_locale][index]

with open(config_file_path, 'wt', encoding='utf-8') as config_file:
    config_contents_text = json.dumps(config_contents, indent=2)
    config_file.write(config_contents_text)