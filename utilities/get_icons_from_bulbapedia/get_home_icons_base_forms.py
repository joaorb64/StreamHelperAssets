import requests
from bs4 import BeautifulSoup as BS
import json
from pathlib import Path
import sys
from copy import deepcopy
import urllib.parse
import os

root_path = "full"
Path(root_path).mkdir(parents=True, exist_ok=True)

with open("../../games/pkmn/base_files/config.json", "rt", encoding="utf-8") as config_file:
    config = json.loads(config_file.read())
    list_pokemon = config["character_to_codename"]

def robust_request(link, timeout=30):
    return_code = 404
    while return_code != 200:
        try:
            response = requests.get(link, timeout=timeout)
            return_code = response.status_code
        except requests.exceptions.ConnectionError:
            return robust_request(link)
    return response

def extract_file_from_bulbagarden_page(filename):
    url = f"https://archives.bulbagarden.net/wiki/File:{filename}"

    page = robust_request(url, timeout=30)
    content = page.text
    soup = BS(content, features="html.parser")
    links = soup.findAll("a")

    for href in links:
        if href.text == filename or href.text == "Full-size image":
            return href["href"]

for pokemon_name in list_pokemon.keys():
    print(pokemon_name, list_pokemon[pokemon_name]["codename"])
    filename = f'HOME{int(list_pokemon[pokemon_name]["codename"]):04}.png'
    file_link=extract_file_from_bulbagarden_page(filename)
    download_target = f'{root_path}/full_{list_pokemon[pokemon_name]["codename"]}_0.png'
    with open(download_target, "wb") as f:
        file = robust_request(file_link)
        f.write(file.content)