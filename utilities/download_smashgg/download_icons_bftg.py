import json
from json import encoder
import requests
from bs4 import BeautifulSoup as BS
from pathlib import Path

game_id = 22156

with open(f"game_data.json", 'rt') as game_data_file:
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

characters_file = requests.get("https://api.smash.gg/characters")

description = "Base config to use this game."
credits = ''
version = "1.0"

characters_file_content = characters_file.json()

characters = characters_file_content.get("entities").get("character")

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

full_config_dict = {
    "name": "Renders",
    "description": "Character renders",
    "prefix": "full_",
    "postfix": "_",
    "type": ["full"],
    "version": version
}

download_dir = "download"

full_dir = f"{download_dir}/full"
Path(full_dir).mkdir(parents=True, exist_ok=True)

icon_dir = f"{download_dir}/base_files/icon"
Path(icon_dir).mkdir(parents=True, exist_ok=True)

bftg_page = requests.get(
    "https://battleforthegrid.com/pages/characters")
bftg_content = bftg_page.text
bftg_soup = BS(bftg_content, features="html.parser")

full_portrait_table = bftg_soup.findAll('img', {'class': f'ranger-img'})

for tag in full_portrait_table:
    character_id = tag["id"].replace("-img", "")
    character_desc = bftg_soup.findAll('div', {'id': f"{character_id}-desc"})
    for div in character_desc:
        name_holder = div.findAll('div', {'class': f'name-holder'})
        if name_holder:
            character_name=name_holder[0].text.splitlines()[1]
    config_dict["character_to_codename"][character_name] = {
        "codename": character_id
    }
    image_filename = f"{full_config_dict['prefix']}{character_id}{full_config_dict['postfix']}0.png"
    with open(f"{full_dir}/{image_filename}", 'wb') as f:
        image_file = requests.get(tag["src"].split("?")[0].replace("//", 'https://'))
        f.write(image_file.content)

icon_table = bftg_soup.findAll('a', {'class': f'characters-slider-link'})

for tag in icon_table:
    list_img=tag.findAll("img")
    for img in list_img:
        character_id = tag["id"]
        image_filename = f"{icon_config_dict['prefix']}{character_id}{icon_config_dict['postfix']}0.png"
        with open(f"{icon_dir}/{image_filename}", 'wb') as f:
            image_file = requests.get(img["src"].split("?")[0].replace("//", 'https://'))
            f.write(image_file.content)

with open(f"{download_dir}/base_files/config.json", 'wt', encoding='utf-8') as f:
    f.write(json.dumps(config_dict, indent=2))

with open(f"{icon_dir}/config.json", 'wt', encoding='utf-8') as f:
    f.write(json.dumps(icon_config_dict, indent=2))

with open(f"{full_dir}/config.json", 'wt', encoding='utf-8') as f:
    f.write(json.dumps(full_config_dict, indent=2))
