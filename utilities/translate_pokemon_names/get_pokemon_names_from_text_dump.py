import json
from copy import deepcopy

lang_list = ["fr", "de", "ko", "ja", "zh_CN", "zh_TW", "it", "es"]
lang_data = {}


for lang in lang_list:
    filename = f"./source/common_{lang}.txt"
    with open(filename, 'rt', encoding="utf-8") as f:
        current_lang_data = f.readlines()
        lang_data[lang] = current_lang_data

filename = f"./source/common_en.txt"
with open(filename, 'rt', encoding="utf-8") as f:
    source_data = f.readlines()

config_file_path = "../../games/pkmn/base_files/config.json"

with open(config_file_path, 'rt', encoding='utf-8') as config_file:
    config_contents_text = config_file.read()
    config_contents = json.loads(config_contents_text)

codenames_dict = config_contents.get("character_to_codename")
for character in codenames_dict.keys():
    print(character)
    for i in range(len(source_data)):
        if source_data[i].strip() == character:
            if not codenames_dict.get(character).get("locale"):
                config_contents["character_to_codename"][character]["locale"] = {}
            for current_locale in lang_list:
                print(lang_data[current_locale][i].strip())
                config_contents["character_to_codename"][character]["locale"][current_locale] = lang_data[current_locale][i].strip()
            break
        i = i+1

with open(config_file_path, 'wt', encoding='utf-8') as config_file:
    config_contents_text = json.dumps(config_contents, indent=2)
    config_file.write(config_contents_text)
