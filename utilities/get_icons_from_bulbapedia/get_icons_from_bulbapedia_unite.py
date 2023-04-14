import requests
from bs4 import BeautifulSoup as BS
import json
from pathlib import Path
import sys
from copy import deepcopy
import urllib.parse
import os

sys.setrecursionlimit(100)

root_path = "punite"
base_files_path = f"{root_path}/base_files"
full_path = f"{root_path}/full"
icon_path = f"{base_files_path}/icon"

with open("_unite_pkmn_list.txt", "rt", encoding="utf-8") as list_unitedex_file:
    list_unitedex = list_unitedex_file.readlines()
    list_unitedex_copy = []
    for pkmn in list_unitedex:
        list_unitedex_copy.append(pkmn.strip())
    list_unitedex = list_unitedex_copy
    print(list_unitedex)

with open("../../games/pkmn/base_files/config.json", "rt", encoding="utf-8") as pkmn_config_file:
    pkmn_config = pkmn_config_file.read()
    pkmn_config = json.loads(pkmn_config)
    natdex = pkmn_config["character_to_codename"]

def get_icon_path_from_dex_number(dex_number):
    icon_path = f"../../games/pkmn/base_files/icon/icon_{int(dex_number):03}_0.png"
    if f"{int(dex_number):03}" in ["888", "038"]:
        icon_path = icon_path.replace('_0.png', "_1.png")
    elif f"{int(dex_number):03}" in ["845"]:
        icon_path = icon_path.replace('_0.png', "_2.png")
    return(icon_path)

def create_folder_structure():
    Path(root_path).mkdir(parents=True, exist_ok=True)
    Path(full_path).mkdir(parents=True, exist_ok=True)
    Path(icon_path).mkdir(parents=True, exist_ok=True)


def robust_request(link, timeout=30):
    return_code = 404
    while return_code != 200:
        try:
            response = requests.get(link, timeout=timeout)
            return_code = response.status_code
        except requests.exceptions.ConnectionError:
            return robust_request(link)
    return response


def generate_main_config_skeleton():
    description = "Base config to use this game."
    credits = ""
    version = "1.0"

    game_id = 38949

    with open(
        f"../download_smashgg/game_data.json", "rt", encoding="utf-8"
    ) as game_data_file:
        game_data = json.loads(game_data_file.read())
    found = False
    for game in game_data:
        if game.get("smashgg_id") == game_id:
            game_name = game.get("name")
            challonge_id = game.get("challonge_id")
            found = True

    if not found:
        print("Game not found")
        exit(1)

    config_dict: dict = {
        "name": str(game_name),
        "smashgg_game_id": game_id,
        "challonge_game_id": challonge_id,
        "character_to_codename": {},
        "stage_to_codename": {},
        "version": version,
        "description": str(description),
        "credits": str(credits),
    }

    return config_dict


def write_configs(config_dict):
    with open(f"{base_files_path}/config.json", "wt", encoding="utf-8") as f:
        f.write(json.dumps(config_dict, indent=2))

    version = config_dict["version"]

    icon_config_dict = {
        "prefix": "icon_",
        "postfix": "_",
        "type": ["icon"],
        "version": version,
    }

    with open(f"{icon_path}/config.json", "wt", encoding="utf-8") as f:
        f.write(json.dumps(icon_config_dict, indent=2))

    portrait_config_dict = {
        "name": "Renders",
        "description": "Character Renders",
        "prefix": "full_",
        "postfix": "_",
        "type": ["full"],
        "credits": "",
        "version": version,
    }

    with open(f"{full_path}/config.json", "wt", encoding="utf-8") as f:
        f.write(json.dumps(portrait_config_dict, indent=2))


def download_item_from_data(pokemon_data):
    dex_number = pokemon_data["codename"]
    icon_filename = f"icon_{dex_number}_0.png"
    with open(f"{icon_path}/{icon_filename}", "wb") as f:
        with open(pokemon_data["icon_file"], 'rb') as source:
            f.write(source.read())
    # portrait_url = pokemon_data["full_url"]
    # portrait_filename = f"full_{dex_number}_0.png"
    # with open(f"{full_path}/{portrait_filename}", "wb") as f:
    #     portrait_file = robust_request(portrait_url)
    #     f.write(portrait_file.content)


def check_file_availability(pokemon_data, dex_number):
    nb_variants = len(pokemon_data["variants"])
    exists = True
    for index in range(nb_variants + 1):
        filename = f"full_{dex_number}_{index}.png"
        file_path = f"{full_path}/{filename}"
        if not (os.path.exists(file_path) and os.path.getsize(file_path) > 0):
            exists = False
    return exists


def extract_file_from_bulbagarden_page(filename):
    url = f"https://archives.bulbagarden.net/wiki/File:{filename}"

    page = robust_request(url, timeout=30)
    content = page.text
    soup = BS(content, features="html.parser")
    links = soup.findAll("a")

    for href in links:
        if href.text == filename or href.text == "Full-size image":
            return href["href"]


create_folder_structure()

unitedex_url = (
    "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_(UNITE)"
)
unitedex_page = robust_request(unitedex_url, timeout=30)
unitedex_content = unitedex_page.text
unitedex_soup = BS(unitedex_content, features="html.parser")
pokemon_tables = unitedex_soup.findAll("table")

pokemon_dict = {}

for table in pokemon_tables:
    dex_flag = False
    img_elements = table.findAll("img")
    for img_element in img_elements:
        if (img_element["alt"].startswith("UNITE ")) and ("License Card" not in img_element["alt"]):
            for pkmn in list_unitedex:
                if img_element["alt"].endswith(f"{pkmn.replace('.', '')}.png"):
                    dex_flag = True
                    break
            break
    if dex_flag:
        for key in natdex:
            if "Ninetales" not in pkmn:
                if pkmn == key:
                    pkmn_data = natdex[key]
            else:
                if "Ninetales" == key:
                    pkmn_data = natdex[key]
        pokemon_dict[pkmn] = {
            "codename": pkmn_data["codename"],
            "icon_file": get_icon_path_from_dex_number(pkmn_data["codename"]),
            "locale": pkmn_data["locale"],
            "full_url": extract_file_from_bulbagarden_page(img_element["alt"].replace(" ", "_"))
            }
        download_item_from_data(pokemon_dict[pkmn])
        pokemon_dict[pkmn].pop("icon_file")
        pokemon_dict[pkmn].pop("full_url")


main_config = generate_main_config_skeleton()
main_config["character_to_codename"] = pokemon_dict

write_configs(main_config)
