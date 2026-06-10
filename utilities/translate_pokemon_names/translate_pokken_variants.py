import requests
import json
from copy import deepcopy

config_file_path = "../../games/pokkendx/base_files/config.json"
pkmn_config_file_path = "../../games/pkmn/base_files/config.json"

with open(config_file_path, 'rt', encoding='utf-8') as config_file:
    config_contents_text = config_file.read()
    config_contents = json.loads(config_contents_text)

variant_dict = config_contents.get("variant_to_codename")

with open(pkmn_config_file_path, 'rt', encoding='utf-8') as pkmn_config_file:
    pkmn_config_contents_text = pkmn_config_file.read()
    pkmn_config_contents = json.loads(pkmn_config_contents_text)

pkmn_dict = pkmn_config_contents.get("character_to_codename")

for variant in variant_dict.keys():
    variant_split = variant.split(" / ")
    i = 0
    for i in range(len(variant_split)):
        if "Rayquaza" in variant_split[i]:
            variant_split[i] = "Rayquaza"
    
    variant_dict[variant]["locale"] = pkmn_dict[variant_split[0]]["locale"]
    if "br" not in variant_dict[variant]["locale"].keys():
        variant_dict[variant]["locale"]["br"] = variant_split[0]

    for locale in variant_dict[variant]["locale"].keys():
        if variant_split[0] == "Rayquaza":
            variant_dict[variant]["locale"][locale] = variant_dict[variant]["locale"][locale] + " (Mega)"
        variant_dict[variant]["locale"][locale] = variant_dict[variant]["locale"][locale] + " / " + pkmn_dict[variant_split[1]]["locale"].get(locale, variant_split[1])
        if variant_split[1] == "Rayquaza":
            variant_dict[variant]["locale"][locale] = variant_dict[variant]["locale"][locale] + " (Mega)"
    

config_contents["variant_to_codename"] = variant_dict

with open(config_file_path, 'wt', encoding='utf-8') as config_file:
    config_contents_text = json.dumps(config_contents, indent=2)
    config_file.write(config_contents_text)