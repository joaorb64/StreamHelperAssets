import requests
from bs4 import BeautifulSoup as BS
import json
from pathlib import Path
from PIL import Image

base_url = "https://www.nintendo.com/jp/games/switch2/aaaba/rider-machine/index.html"

page = requests.get(base_url)
content = page.text
soup = BS(content, features="html.parser")
section_tags = soup.findAll("section")



game_id = 102561

download_folder_name = "../download_smashgg/download"
base_files_folder_name = f"{download_folder_name}/base_files"
portraits_folder_name = f"{download_folder_name}/full"
variant_folder_name = f"{download_folder_name}/variant_icon"
icon_folder_name = f"{base_files_folder_name}/icon"
for folder_name in (download_folder_name, base_files_folder_name, portraits_folder_name, icon_folder_name, variant_folder_name):
    Path(folder_name).mkdir(parents=True, exist_ok=True)

def download_webp_as_png(uri, filename, directory):
    url = uri.replace("../", "https://www.nintendo.com/jp/games/switch2/aaaba/")
    response = requests.get(url, stream=True)
    image = Image.open(response.raw).convert("RGBA")
    image.save(f"{directory}/{filename}.png")

def generate_configs():
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
    credits = f'Assets ripped from {base_url}'
    version = "1.0"

    config_dict: dict = {
        "name": str(game_name),
        "smashgg_game_id": game_id,
        "challonge_game_id": challonge_id,
        "character_to_codename": {},
        "stage_to_codename": {},
        "variant_to_codename": {},
        "version": version,
        "description": str(description),
        "credits": str(credits)
    }

    icon_config_dict = {
        "prefix": "icon_",
        "postfix": "_",
        "type": ["icon"],
        "version": version,
        "uncropped_edge": [
            "u",
            "d",
            "l",
            "r"
        ]
    }

    portrait_config_dict = {
        "name": "Renders",
        "description": "Character renders",
        "prefix": "full_",
        "postfix": "_",
        "type": ["full"],
        "credits": str(credits),
        "version": version,
        "uncropped_edge": [
            "u",
            "d",
            "l",
            "r"
        ]
    }
    
    variant_config_dict = {
        "name": "Machines",
        "description": "Machine renders",
        "prefix": "var_",
        "postfix": "",
        "type": ["variant_icon"],
        "credits": str(credits),
        "version": version
    }

    with open("id_to_character.json", "rt", encoding="utf-8") as file:
        codename_dict = json.loads(file.read())
        for codename in codename_dict.keys():
            config_dict["character_to_codename"][codename_dict.get(codename)] = {
                "codename": codename
            }

    
    with open("id_to_variant.json", "rt", encoding="utf-8") as file:
        codename_dict = json.loads(file.read())
        for codename in codename_dict.keys():
            config_dict["variant_to_codename"][codename_dict.get(codename)] = {
                "codename": codename
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
        
    with open(f"{variant_folder_name}/config.json", 'wt') as variant_config_file:
        variant_config_file_content = json.dumps(
            variant_config_dict, indent=2)
        variant_config_file.write(variant_config_file_content)

    return config_dict, icon_config_dict, portrait_config_dict, variant_config_dict


def get_portraits(config_dict, portrait_config_dict):
    print("Get portraits")

    chara_list = config_dict["character_to_codename"]

    for section_tag in section_tags:
        if section_tag.get("id") == "rider":
            portrait_tags = section_tag.findAll("ul", {"class": "kbar-rm-rider-info-chara"})
            portrait_tags = portrait_tags[0].findAll("li")

            for character in chara_list.keys():
                print(character)
                codename = chara_list.get(character).get("codename")

                for portrait_tag in portrait_tags:
                    if codename in str(portrait_tag.get("class")):
                        image_tags = portrait_tag.findAll("img")
                        index = 0
                        for image_tag in image_tags:
                            filename = f"{portrait_config_dict.get('prefix')}{codename}{portrait_config_dict.get('postfix')}{index:02}"
                            uri = image_tag.get("src")
                            download_webp_as_png(uri, filename, portraits_folder_name)
                            index += 1


def get_icons(config_dict, icon_config_dict):
    print("Get icons")
    chara_list = config_dict["character_to_codename"]

    for section_tag in section_tags:
        if section_tag.get("id") == "rider":
            icon_tags = section_tag.findAll("div", {"class": "kbar-rm-rider-info-color"})
            icon_tags = icon_tags[0].findAll("ul")

            for character in chara_list.keys():
                print(character)
                codename = chara_list.get(character).get("codename")

                for icon_tag in icon_tags:
                    if codename in str(icon_tag.get("class")):
                        image_tags = icon_tag.findAll("img")
                        index = 0
                        for image_tag in image_tags:
                            filename = f"{icon_config_dict.get('prefix')}{codename}{icon_config_dict.get('postfix')}{index:02}"
                            uri = image_tag.get("src")
                            download_webp_as_png(uri, filename, icon_folder_name)
                            index += 1


def get_variants(config_dict, variant_config_dict):
    print("Get variants")
    variant_list = config_dict["variant_to_codename"]

    for section_tag in section_tags:
        if section_tag.get("id") == "machine":
            portrait_tags = section_tag.findAll("ul", {"class": "kbar-rm-machine-info-chara"})
            portrait_tags = portrait_tags[0].findAll("li")

            for variant in variant_list.keys():
                print(variant)
                codename = variant_list.get(variant).get("codename")

                for portrait_tag in portrait_tags:
                    if codename in str(portrait_tag.get("class")):
                        image_tags = portrait_tag.findAll("img")
                        for image_tag in image_tags:
                            filename = f"{variant_config_dict.get('prefix')}{codename}{variant_config_dict.get('postfix')}"
                            uri = image_tag.get("src")
                            download_webp_as_png(uri, filename, variant_folder_name)


config_dict, icon_config_dict, portrait_config_dict, variant_config_dict = generate_configs()
get_icons(config_dict, icon_config_dict)
get_portraits(config_dict, portrait_config_dict)
get_variants(config_dict, variant_config_dict)