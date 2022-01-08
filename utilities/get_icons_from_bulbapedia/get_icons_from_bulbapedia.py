import requests
from bs4 import BeautifulSoup as BS
import json
from pathlib import Path
import sys
from copy import deepcopy
import urllib.parse
import os

sys.setrecursionlimit(100)

root_path = "pkmn"
base_files_path = f"{root_path}/base_files"
full_path = f"{root_path}/full"
icon_path = f"{base_files_path}/icon"


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

    game_id = 15486

    with open(
        f"../download_smashgg/game_data.json", "rt", encoding="utf-8"
    ) as game_data_file:
        game_data = json.loads(game_data_file.read())
    found = False
    for game in game_data:
        if game.get("smashgg_id") == game_id:
            game_name = game.get("name")
            found = True

    if not found:
        print("Game not found")
        exit(1)

    config_dict: dict = {
        "name": str(game_name),
        "smashgg_game_id": game_id,
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
        "name": "Pokémon Home sprites",
        "description": "Pokémon Home sprites",
        "prefix": "full_",
        "postfix": "_",
        "type": ["full"],
        "credits": "",
        "version": version,
    }

    with open(f"{full_path}/config.json", "wt", encoding="utf-8") as f:
        f.write(json.dumps(portrait_config_dict, indent=2))


def download_item_from_data(pokemon_data, dex_number):
    icon_url = pokemon_data["icon"]
    icon_filename = f"icon_{dex_number}_0.png"
    with open(f"{icon_path}/{icon_filename}", "wb") as f:
        icon_file = robust_request(icon_url)
        f.write(icon_file.content)
    portrait_url = pokemon_data["portrait"]
    portrait_filename = f"full_{dex_number}_0.png"
    with open(f"{full_path}/{portrait_filename}", "wb") as f:
        portrait_file = robust_request(portrait_url)
        f.write(portrait_file.content)

    index = 1
    for variant in pokemon_data["variants"]:
        icon_url = variant["icon"]
        icon_filename = f"icon_{dex_number}_{index}.png"
        with open(f"{icon_path}/{icon_filename}", "wb") as f:
            icon_file = robust_request(icon_url)
            f.write(icon_file.content)
        portrait_url = variant["portrait"]
        portrait_filename = f"full_{dex_number}_{index}.png"
        with open(f"{full_path}/{portrait_filename}", "wb") as f:
            portrait_file = robust_request(portrait_url)
            f.write(portrait_file.content)
        index += 1


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


def detect_variants(dex_page_url, dex_name, dex_number):
    suffix_database = {
        "Galarian": {"suffix": "G", "gen": 8},
        "Alolan": {"suffix": "A", "gen": 7},
        "Gigantamax": {"suffix": "Gi", "gen": 8},
        "Mega": {"suffix": "M", "gen": 6},
        "Primal": {"suffix": "P", "gen": 6},
        "Eternamax": {"suffix": "E", "gen": 8},
    }

    skip_list = [849, 892]

    variants = []

    dex_page = robust_request(dex_page_url, timeout=30)
    dex_content = dex_page.text
    dex_soup = BS(dex_content, features="html.parser")
    tables = dex_soup.findAll("table")

    if int(dex_number) not in skip_list:
        for variant in suffix_database.keys():
            variant_exists = False
            special_mega = False
            for table in tables:
                a_elements = table.findAll("a")
                for a_element in a_elements:
                    try:
                        if f"{variant} {dex_name}" in a_element["title"]:
                            variant_exists = True
                            if f"{dex_name} X" in a_element["title"]:
                                special_mega = True
                            break
                    except KeyError:
                        None
                    if variant_exists:
                        break
            if variant_exists:
                if variant == "Mega" and special_mega:
                    for type in ["X", "Y"]:
                        icon_filename = f"{dex_number}{suffix_database[variant]['suffix']}{type}MS{suffix_database[variant]['gen']}.png"
                        icon_url = extract_file_from_bulbagarden_page(icon_filename)
                        portrait_filename = f"HOME{dex_number}{suffix_database[variant]['suffix']}{type}.png"
                        portrait_url = extract_file_from_bulbagarden_page(
                            portrait_filename
                        )

                        variants.append({"icon": icon_url, "portrait": portrait_url})
                else:
                    default_icon_filename = f"{dex_number}{suffix_database[variant]['suffix']}MS{suffix_database[variant]['gen']}.png"
                    list_godex = [19, 20, 74, 75, 76, 88, 89]
                    list_galardex = [
                        26,
                        27,
                        28,
                        37,
                        38,
                        50,
                        51,
                        52,
                        53,
                        77,
                        78,
                        103,
                        105,
                        110,
                    ]
                    if variant == "Alolan":
                        if (int(dex_number) not in list_galardex) and (
                            int(dex_number) not in list_godex
                        ):
                            icon_filename = default_icon_filename
                        elif int(dex_number) in list_godex:
                            icon_filename = f"{dex_number}{suffix_database[variant]['suffix']}MSPE.png"
                        elif int(dex_number) in list_galardex:
                            icon_filename = f"{dex_number}{suffix_database[variant]['suffix']}MS8.png"
                    elif variant == "Gigantamax":
                        if int(dex_number) == 842:
                            icon_filename = f"841{suffix_database[variant]['suffix']}MS8.png"
                        else:
                            icon_filename = default_icon_filename
                    else:
                        icon_filename = default_icon_filename
                    icon_url = extract_file_from_bulbagarden_page(icon_filename)
                    if variant == "Gigantamax" and int(dex_number) == 842:
                        portrait_filename = f"HOME841{suffix_database[variant]['suffix']}.png"
                    else:
                        portrait_filename = f"HOME{dex_number}{suffix_database[variant]['suffix']}.png"
                    portrait_url = extract_file_from_bulbagarden_page(portrait_filename)

                    variants.append({"icon": icon_url, "portrait": portrait_url})

    return variants


def download_special(pokemon_list):
    with open("_special.json", "rt", encoding="utf-8") as f:
        special_forms = json.loads(f.read())
    for dex_num in special_forms.keys():
        print(dex_num)
        index = len(pokemon_list[dex_num]["variants"]) + 1
        variant_list = special_forms[dex_num]
        for variant in variant_list:
            icon_filename = f"icon_{dex_num}_{index}.png"
            icon_url = extract_file_from_bulbagarden_page(variant.get("iconfile"))
            file_path = f"{icon_path}/{icon_filename}"
            if not (os.path.exists(file_path) and os.path.getsize(file_path) > 0):
                with open(file_path, "wb") as f:
                    icon_file = robust_request(icon_url)
                    f.write(icon_file.content)

            portrait_remote_filename = f'HOME{dex_num}{variant.get("suffix")}.png'
            portrait_url = extract_file_from_bulbagarden_page(portrait_remote_filename)
            portrait_filename = f"full_{dex_num}_{index}.png"
            file_path = f"{full_path}/{portrait_filename}"
            if not (os.path.exists(file_path) and os.path.getsize(file_path) > 0):
                with open(file_path, "wb") as f:
                    portrait_file = robust_request(portrait_url)
                    f.write(portrait_file.content)

            index += 1


create_folder_structure()

natdex_url = (
    "https://bulbapedia.bulbagarden.net/wiki/List_of_Pokémon_by_National_Pokédex_number"
)
natdex_page = robust_request(natdex_url, timeout=30)
natdex_content = natdex_page.text
natdex_soup = BS(natdex_content, features="html.parser")
pokemon_tables = natdex_soup.findAll("table")

pokemon_tables_copy = []

for table in pokemon_tables:
    dex_flag = False
    tr_elements = table.findAll("tr")
    for tr_element in tr_elements:
        if "Ndex" in tr_element.text:
            dex_flag = True
            break
    if dex_flag:
        pokemon_tables_copy.append(table)

pokemon_tables = pokemon_tables_copy

print(len(pokemon_tables))


pokemon_list_file = "_list.json"

try:
    with open(pokemon_list_file, "rt", encoding="utf-8") as f:
        pokemon_list = json.loads(f.read())
except:
    pokemon_list = {}

main_config = generate_main_config_skeleton()

for table in pokemon_tables:
    tr_elements = table.findAll("tr")
    for tr_element in tr_elements:
        if "Ndex" not in tr_element.text:
            td_elements = tr_element.findAll("td")
            dex_number = td_elements[1].text.replace("#", "").strip()
            if (dex_number not in pokemon_list.keys()) and ("-" not in dex_number):
                dex_name = td_elements[2].text.strip()
                print(f"{dex_number}: {dex_name}")
                img_elements = tr_element.findAll("img")
                dex_icon = f'https:{img_elements[0]["src"]}'
                dex_name_parse = urllib.parse.quote(dex_name)
                portrait_filename = f"HOME{dex_number}.png"
                portrait_url = extract_file_from_bulbagarden_page(portrait_filename)
                dex_page = f'https://bulbapedia.bulbagarden.net/wiki/{dex_name_parse}_({urllib.parse.quote("Pokémon")})'

                variants = detect_variants(dex_page, dex_name, dex_number)

                pokemon_list[dex_number] = {
                    "name": dex_name,
                    "icon": dex_icon,
                    "portrait": portrait_url,
                    "variants": variants,
                }

                # print(pokemon_list[dex_number])

                if not check_file_availability(pokemon_list[dex_number], dex_number):
                    download_item_from_data(pokemon_list[dex_number], dex_number)

                with open(pokemon_list_file, "wt", encoding="utf-8") as f:
                    f.write(json.dumps(pokemon_list, indent=2))

            if "-" not in dex_number:
                main_config["character_to_codename"][pokemon_list[dex_number]["name"]] = {
                    "codename": dex_number
                }

download_special(pokemon_list)

write_configs(main_config)
