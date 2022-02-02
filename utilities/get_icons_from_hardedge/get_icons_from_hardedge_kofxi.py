import requests
from bs4 import BeautifulSoup as BS
import json
from pathlib import Path
import sys

def robust_request(link):
    return_code = 404
    while return_code != 200:
        try:
            response = requests.get(link, timeout=30)
            return_code = response.status_code
        except requests.exceptions.ConnectionError:
            return(robust_request(link))
    return(response)

def get_portrait_link_from_wiki(wiki_link):
    wiki_page = robust_request(wiki_link)
    wiki_content = wiki_page.text
    wiki_soup = BS(wiki_content, features="html.parser")
    images = wiki_soup.findAll('img')
    for image in images:
        if "KOFXI" in image["alt"] and "full.png" in image["alt"]:
            return(image["src"])

sys.setrecursionlimit(100)

hardedge_page = requests.get(
    "https://wiki.hardedge.org/wiki/The_King_of_Fighters_XI", timeout=30)
hardedge_content = hardedge_page.text
hardedge_soup = BS(hardedge_content, features="html.parser")
element_table = hardedge_soup.findAll('a')

characters = {}

for element in element_table:
    try:
        link = f'https://wiki.hardedge.org{element["href"]}'
        if "(KOFXI)" in link and "/wiki/" in link:
            character = element["title"].replace("(KOFXI)", "")
            images = element.findAll('img')
            if images:
                for image in images:
                    image_link = image["src"]
            portrait_link = get_portrait_link_from_wiki(link)
            characters[character] = {
                "codename": character.replace(' ', '').replace('&', '').replace('.', '').replace('(', '').replace(')', '').replace('-', '').replace("'", ''),
                "portrait_url": f'https://wiki.hardedge.org{portrait_link}',
                "icon_url": f'https://wiki.hardedge.org{image_link}'
            }
    except KeyError:
        None

print(json.dumps(characters, indent=2))

game_id = 34054

download_folder_name = "../download_smashgg/download"
base_files_folder_name = f"{download_folder_name}/base_files"
portraits_folder_name = f"{download_folder_name}/full"
icon_folder_name = f"{base_files_folder_name}/icon"
for folder_name in (download_folder_name, base_files_folder_name, portraits_folder_name, icon_folder_name):
    Path(folder_name).mkdir(parents=True, exist_ok=True)

def generate_configs(character_dict):
    with open(f"../download_smashgg/game_data.json", 'rt') as game_data_file:
        game_data = json.loads(game_data_file.read())
    found = False
    for game in game_data:
        if game.get("smashgg_id") == game_id:
            game_name = game.get("name")
            image_type = game.get("image_type")
            challonge_id = game.get("challonge_id")
            found = True

    if not found:
        print("Game not found")
        exit(1)

    description = "Base config to use this game."
    credits = 'Files ripped from Hardedge Wiki'
    version = "1.0"

    config_dict: dict = {
        "name": str(game_name),
        "smashgg_game_id": game_id,
        "challonge_game_id": challonge_id,
        "character_to_codename": {},
        "stage_to_codename": {},
        "version": version,
        "description": str(description),
        "credits": str(credits)
    }

    icon_config_dict = {
        "prefix": "icon_",
        "postfix": "_",
        "type": ["icon"],
        "version": version
    }

    portrait_config_dict = {
        "name": "Portraits",
        "description": "Character portraits",
        "prefix": "full_",
        "postfix": "_",
        "type": ["full"],
        "credits": "",
        "version": "1.0"
    }

    for character_name in character_dict.keys():
        config_dict["character_to_codename"][character_name] = {
            "codename": character_dict.get(character_name).get("codename")
        }

    with open(f"{base_files_folder_name}/config.json", 'wt') as main_config_file:
        config_file_content = json.dumps(config_dict, indent=2)
        main_config_file.write(config_file_content)

    with open(f"{icon_folder_name}/config.json", 'wt') as icon_config_file:
        icon_config_file_content = json.dumps(icon_config_dict, indent=2)
        icon_config_file.write(icon_config_file_content)

    with open(f"{portraits_folder_name}/config.json", 'wt') as portrait_config_file:
        portrait_config_file_content = json.dumps(
            portrait_config_dict, indent=2)
        portrait_config_file.write(portrait_config_file_content)

    return config_dict, icon_config_dict, portrait_config_dict

def download_all_images(character_dict: dict, icon_config_dict, portrait_config_dict):
    print(character_dict)
    for character_name in character_dict.keys():
        print(character_name)
        character_data = character_dict.get(character_name)
        icon_filename = f'{icon_folder_name}/{icon_config_dict.get("prefix")}{character_data.get("codename")}{icon_config_dict.get("postfix")}0.png'
        portrait_filename = f'{portraits_folder_name}/{portrait_config_dict.get("prefix")}{character_data.get("codename")}{portrait_config_dict.get("postfix")}0.png'
        with open(icon_filename, 'wb') as f:
            icon_file = robust_request(character_data.get("icon_url"))
            f.write(icon_file.content)
        with open(portrait_filename, 'wb') as f:
            portrait_file = robust_request(character_data.get("portrait_url"))
            f.write(portrait_file.content)
            
main_config_dict, icon_config_dict, portrait_config_dict = generate_configs(
    characters)
download_all_images(characters, icon_config_dict, portrait_config_dict)
