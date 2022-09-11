from email.mime import image
import requests
from bs4 import BeautifulSoup as BS
import json
from pathlib import Path
import sys
from copy import deepcopy
import urllib.parse
import os

sys.setrecursionlimit(100)

root_path = "spl3"
base_files_path = f"{root_path}/base_files"
full_path = f"{root_path}/full"
icon_path = f"{base_files_path}/icon"
stage_path = f"{root_path}/stage_icon"


def create_folder_structure():
    Path(root_path).mkdir(parents=True, exist_ok=True)
    # Path(full_path).mkdir(parents=True, exist_ok=True)
    Path(icon_path).mkdir(parents=True, exist_ok=True)
    Path(stage_path).mkdir(parents=True, exist_ok=True)


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

    game_id = 36202

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

    stage_config = {
        "name": "Stage Icons",
        "version": "1.0",
        "description": "Stage icons",
        "prefix": "stage_",
        "postfix": "",
        "type": [
            "stage_icon"
        ]
    }

    with open(f"{stage_path}/config.json", "wt", encoding="utf-8") as f:
        f.write(json.dumps(stage_config, indent=2))


create_folder_structure()

weapon_page = (
    "https://splatoonwiki.org/wiki/List_of_weapons_in_Splatoon_3"
)
weapon_page = robust_request(weapon_page, timeout=30)
weapon_content = weapon_page.text
weapon_soup = BS(weapon_content, features="html.parser")
weapon_tables = weapon_soup.findAll("table")
weapon_body_tag = None
for table in weapon_tables:
    tbody_list = table.findAll('tbody')
    for tbody in tbody_list:
        if ".52 Gal" in str(tbody):
            weapon_body_tag = tbody
            break
    if weapon_body_tag:
        break

weapon_body_images = weapon_body_tag.findAll('img')

weapon_list = {}

for image_tag in weapon_body_images:
    if "S3_Weapon_Main" in image_tag["src"]:
        weapon_name = image_tag["alt"]
        weapon_name = weapon_name.replace("S3 Weapon Main ", "")
        weapon_name = weapon_name.replace(" Flat.png", "")
        weapon_link = f'https:{image_tag["src"]}'
        weapon_link = weapon_link.replace(weapon_link.split('/')[-1], "")
        weapon_link = weapon_link.replace("/thumb", "")
        weapon_link = weapon_link.strip("/")
        weapon_list[weapon_name] = weapon_link

print(json.dumps(weapon_list, indent=2))
print(len(weapon_list))

main_config = generate_main_config_skeleton()

for weapon_name in weapon_list.keys():
    icon_url = weapon_list[weapon_name]
    weapon_codename = weapon_name.replace(".", "")
    weapon_codename = weapon_codename.replace(" ", "")
    weapon_codename = weapon_codename.replace("-", "")
    icon_filename = f"icon_{weapon_codename}_0.png"
    with open(f"{icon_path}/{icon_filename}", "wb") as f:
        icon_file = robust_request(icon_url)
        f.write(icon_file.content)
    main_config["character_to_codename"][weapon_name] = {"codename": weapon_codename}


write_configs(main_config)
