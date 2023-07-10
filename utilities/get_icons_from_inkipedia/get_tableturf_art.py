import requests
from bs4 import BeautifulSoup as BS
import json
from pathlib import Path
import sys
from PIL import Image

sys.setrecursionlimit(100)


def robust_request(link, timeout=30, recursion=30):
    try:
        response = requests.get(link, timeout=timeout)
        return_code = response.status_code
        if return_code != 200 and recursion > 0:
            return robust_request(link, timeout, recursion-1)
        else:
            return response
    except requests.exceptions.ConnectionError:
        return robust_request(link, timeout, recursion-1)
    
def convert_thumb_link_to_image_link(thumb_link):
    thumb_link = f'https:{thumb_link}'
    thumb_link = thumb_link.replace(thumb_link.split('/')[-1], "")
    thumb_link = thumb_link.replace("/thumb", "")
    thumb_link = thumb_link.strip("/")
    return thumb_link


root_path = "spl3"
base_files_path = f"{root_path}/base_files"
main_config_path = f"{base_files_path}/config.json"
with open(main_config_path, 'rt', encoding='utf-8') as main_config_file:
    main_config_dict = json.loads(main_config_file.read())
card_path = f"{root_path}/card"
Path(card_path).mkdir(parents=True, exist_ok=True)

card_config_dict = {
    "name": "Tableturf Art",
    "version": main_config_dict["version"],
    "description": "Art used in the Tableturf Battle mode",
    "prefix": "card_",
    "postfix": "_",
    "type": ["card"],
    "uncropped_edge": ["u","d","l","r"],
    "rescaling_factor": {}
}

card_list_url = "https://splatoonwiki.org/wiki/List_of_Tableturf_Battle_cards_in_Splatoon_3"
card_page = robust_request(card_list_url, timeout=30)
card_page_content = card_page.text
card_page_soup = BS(card_page_content, features="html.parser")
card_tables = card_page_soup.findAll("table")
card_body_tag = None
for table in card_tables:
    tbody_list = table.findAll('tbody')
    for tbody in tbody_list:
        if ".52 Gal" in str(tbody):
            card_body_tag = tbody
            break
    if card_body_tag:
        break

card_body_images = card_body_tag.findAll('img')

count = 0
list_weapons = main_config_dict["character_to_codename"].keys()
for weapon in list_weapons:
    found = False
    for image_tag in card_body_images:
        alt_text = image_tag["alt"]
        if ((alt_text.lower() in weapon.lower() and weapon.lower() in alt_text.lower()) 
            or ("Hero" in alt_text and "Hero" in weapon) 
            or ("Noueveau" in alt_text and "Nouveau" in weapon and "Dapple" in weapon)
            or ("Tentatek Splatteershot" in alt_text and "Tentatek Splattershot" in weapon)):
            found = True
            count += 1
            thumb_link = image_tag["src"]
            image_link = convert_thumb_link_to_image_link(thumb_link)
            image_response = robust_request(image_link)
            weapon_codename = main_config_dict["character_to_codename"][weapon]["codename"]
            image_filename = f"card_{weapon_codename}_0.png"
            with open(f"{card_path}/{image_filename}", "wb") as f:
                f.write(image_response.content)
            with Image.open(f"{card_path}/{image_filename}") as image_contents:
                image_height = image_contents.height
                ratio = 512.0/float(image_height)
                if ratio != 1.0:
                    card_config_dict["rescaling_factor"][weapon_codename] = {"0": ratio}

    if not found:
        print("Not found:", weapon)

with open(f"{card_path}/config.json", "wt", encoding="utf-8") as f:
    f.write(json.dumps(card_config_dict, indent=2))