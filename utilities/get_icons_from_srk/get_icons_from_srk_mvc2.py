import requests
from bs4 import BeautifulSoup as BS
import json
from pathlib import Path

base_url = "https://srk.shib.live/w/Marvel_vs_Capcom_2"

srk_page = requests.get(base_url)
srk_content = srk_page.text
srk_soup = BS(srk_content, features="html.parser")

parse_tables = srk_soup.findAll('tr')
character_icons_table = []
for tag in parse_tables:
    if ("Akuma" in str(tag)) or ("Colossus" in str(tag)):
        character_icons_table = character_icons_table + tag.findAll(
            'span', {'style': f'text-align:center; float:left; overflow:hidden; margin-top: 5px; margin-right: 1px;'})

game_id = 1731

download_folder_name = "../download_smashgg/download"
base_files_folder_name = f"{download_folder_name}/base_files"
portraits_folder_name = f"{download_folder_name}/full"
icon_folder_name = f"{base_files_folder_name}/icon"
for folder_name in (download_folder_name, base_files_folder_name, portraits_folder_name, icon_folder_name):
    Path(folder_name).mkdir(parents=True, exist_ok=True)


def get_icon_from_character_name(character_name):
    list_img_tags = srk_soup.findAll("img")
    for tag in list_img_tags:
        try:
            alt_text = tag["alt"]
        except:
            alt_text = None
        if (character_name in alt_text) and ("Portrait" in tag["src"]):
            return(f'https://srk.shib.live{tag["src"]}')


def get_portrait(character_name, page_link):
    character_page = requests.get(page_link)
    character_page_soup = BS(character_page.text, features="html.parser")
    character_page_links_tag_list = character_page_soup.findAll('a', href=True)
    portrait_wiki_link = None
    for tag in character_page_links_tag_list:
        link = tag["href"]
        if ("_art" in link) and ("File:MVC2" in link):
            portrait_wiki_link = link
    if portrait_wiki_link:
        portrait_wiki_page = requests.get(
            f"https://srk.shib.live{portrait_wiki_link}")
        portrait_wiki_soup = BS(portrait_wiki_page.text, features="html.parser")
        portrait_page_links_tag_list = portrait_wiki_soup.findAll('a', href=True)
        # print(portrait_page_links_tag_list)
        for tag in portrait_page_links_tag_list:
            text = tag.get_text()
            link = tag["href"]
            if (("Original file" in text) or (".png" in text)) and "_art" in link:
                break
        return(f"https://srk.shib.live{link}")


def get_all_links():
    list_characters = []
    list_characters_page = []

    for character_tag in character_icons_table:
        href_tags = character_tag.findAll('a', href=True)
        for href_tag in href_tags:
            if "Marvel vs Capcom 2/" in href_tag["title"]:
                list_characters_page.append(f'https://srk.shib.live{href_tag["href"]}')
                list_characters.append(href_tag.text.lstrip().rstrip())

    character_dict = {}

    for i in range(len(list_characters)):
        icon_link = get_icon_from_character_name(
            list_characters[i].encode("ascii", "ignore").decode())
        portrait_link = get_portrait(
            list_characters[i], list_characters_page[i])
        character_dict[list_characters[i].encode("ascii", "ignore").decode()] = {
            "codename": list_characters[i].replace(' ', '').replace('&', '').replace('.', '').replace('(', '').replace(')', '').replace('-', '').replace("'", ''),
            "portrait_url": portrait_link,
            "icon_url": icon_link
        }

    return(character_dict)


def generate_configs(character_dict):
    with open(f"../download_smashgg/game_data.json", 'rt') as game_data_file:
        game_data = json.loads(game_data_file.read())
    found = False
    for game in game_data:
        if game.get("smashgg_id") == game_id:
            game_name = game.get("name")
            image_type = game.get("image_type")
            found = True

    if not found:
        print("Game not found")
        exit(1)

    description = "Base config to use this game."
    credits = 'Assets ripped from SRK Wiki (https://srk.shib.live/w/Marvel_vs_Capcom_2)'
    version = "1.0"

    config_dict: dict = {
        "name": str(game_name),
        "smashgg_game_id": game_id,
        "character_to_codename": {},
        "stage_to_codename": {},
        "version": version,
        "description": str(description),
        "credits": str(credits)
    }

    readme_file_content = f"""
    # {game_name}

    ## Description:
    {description}

    ## Credits:
    {credits}
    """.replace("    ", "")
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
        "credits": str(credits),
        "version": "1.0"
    }

    for character_name in character_dict.keys():
        config_dict["character_to_codename"][character_name] = {
            "codename": character_dict.get(character_name).get("codename")
        }

    with open(f"{base_files_folder_name}/config.json", 'wt') as main_config_file:
        config_file_content = json.dumps(config_dict, indent=2)
        main_config_file.write(config_file_content)

    with open(f"{download_folder_name}/README.md", 'wt') as readme_file:
        readme_file.write(readme_file_content)

    with open(f"{icon_folder_name}/config.json", 'wt') as icon_config_file:
        icon_config_file_content = json.dumps(icon_config_dict, indent=2)
        icon_config_file.write(icon_config_file_content)

    with open(f"{portraits_folder_name}/config.json", 'wt') as portrait_config_file:
        portrait_config_file_content = json.dumps(
            portrait_config_dict, indent=2)
        portrait_config_file.write(portrait_config_file_content)

    return config_dict, icon_config_dict, portrait_config_dict


def download_all_images(character_dict: dict, icon_config_dict, portrait_config_dict):
    for character_name in character_dict.keys():
        character_data = character_dict.get(character_name)
        icon_filename = f'{icon_folder_name}/{icon_config_dict.get("prefix")}{character_data.get("codename")}{icon_config_dict.get("postfix")}0.png'
        portrait_filename = f'{portraits_folder_name}/{portrait_config_dict.get("prefix")}{character_data.get("codename")}{portrait_config_dict.get("postfix")}0.png'
        with open(icon_filename, 'wb') as f:
            icon_file = requests.get(character_data.get("icon_url"))
            f.write(icon_file.content)
        if character_data.get("portrait_url"):
            with open(portrait_filename, 'wb') as f:
                portrait_file = requests.get(character_data.get("portrait_url"))
                f.write(portrait_file.content)

character_dict = get_all_links()
print(json.dumps(character_dict, indent=2))
main_config_dict, icon_config_dict, portrait_config_dict = generate_configs(character_dict)
download_all_images(character_dict, icon_config_dict, portrait_config_dict)
