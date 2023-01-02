import requests
from bs4 import BeautifulSoup as BS
import json
from pathlib import Path
from copy import deepcopy

config_path = "../../games/pkmn/base_files/config.json"
icon_path = "../../games/pkmn/base_files/icon/icon_{dex}_0.png"

def robust_request(link, timeout=30, iter_remain=100):
    return_code = 403
    while return_code != 200 and return_code != 404 and iter_remain > 0:
        try:
            response = requests.get(link, timeout=timeout)
            return_code = response.status_code
        except requests.exceptions.ConnectionError:
            if iter_remain > 0:
                return robust_request(link, timeout=timeout, iter_remain=iter_remain-1)
            else:
                return(requests.get(link, timeout=timeout))
    return response

def parse_page(url):
    page_request = robust_request(url, timeout=30)
    content = page_request.text
    if page_request.status_code == 200:
        soup = BS(content, features="html.parser")
    else:
        soup = None
    return(soup, page_request.status_code)

def find_correct_image_url(dex_number):
    base_url = "https://www.pokepedia.fr/Fichier:Miniature_{dex}_{game}.png"
    game_list = ["DEPS", "EV"]
    actual_dex_number = dex_number
    if int(dex_number) in [1007]:
        actual_dex_number = f"{dex_number}_Finale"
    if int(dex_number) in [1008]:
        actual_dex_number = f"{dex_number}_Ultime"
    if int(dex_number) in [492]:
        actual_dex_number = f"{dex_number}_Terrestre"
    if int(dex_number) in [916]:
        actual_dex_number = f"{dex_number}_♂"
    while len(str(actual_dex_number)) < 3:
        actual_dex_number = f"0{actual_dex_number}"
    image_url = None
    for game in game_list:
        current_url = base_url.replace("{dex}", actual_dex_number).replace("{game}", game)
        soup, status_code = parse_page(current_url)
        if status_code == 200:
            tag_list = soup.findAll('a', href=True)
            for tag in tag_list:
                link = tag["href"]
                if (f"{game}.png" in link) and ("/images/" in link) and ("Miniature" in link) and (actual_dex_number in link):
                    image_url = f"https://www.pokepedia.fr{link}"
    return(image_url)

with open(config_path, "rt", encoding="utf-8") as f:
    list_pokemon = json.loads(f.read())["character_to_codename"]

for pokemon in list_pokemon:
    dex_number = list_pokemon[pokemon]["codename"]
    image_url = find_correct_image_url(dex_number)
    print(pokemon)
    if image_url:
        with open(icon_path.replace("{dex}", dex_number), "wb") as f:
            image_request = robust_request(image_url)
            f.write(image_request.content)
