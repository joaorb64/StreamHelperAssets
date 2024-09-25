import requests
from bs4 import BeautifulSoup as BS
import json
from pathlib import Path
import sys
from copy import deepcopy
import urllib.parse
import os
from PIL import Image
import io
from multiprocessing.pool import Pool

sys.setrecursionlimit(100)

root_path = "mk1"
costumes = f"{root_path}/costume"


def create_folder_structure():
    Path(costumes).mkdir(parents=True, exist_ok=True)


def robust_request(link, timeout=30):
    return_code = 404
    while return_code != 200:
        try:
            try:
                try:
                    response = requests.get(link, timeout=timeout)
                    return_code = response.status_code
                except requests.exceptions.ConnectionError:
                    return robust_request(link)
            except requests.Timeout:
                return robust_request(link)
        except requests.exceptions.ReadTimeout:
            return robust_request(link)
    return response

def save_character_costumes(character):
    character_page = robust_request(mk1_links[character], timeout=30)
    character_content = character_page.text
    character_soup = BS(character_content, features="html.parser")
    skin_table = character_soup.findAll("div", {"id": "skins"})
    skin_body = skin_table[0].findAll("div", {"class": "body"})
    skin_img = skin_body[0].findAll("img")
    print(character, len(skin_img))
    skin_index = 0
    for index in range(len(skin_img)):
        filename = f"{costumes}/file_{character}_{str(skin_index).zfill(4)}.png"
        img_link = f'https://www.mortalkombatwarehouse.com{skin_img[index]["src"]}'
        if "KAM" not in img_link:
            img_request = robust_request(img_link)
            image_data = Image.open(io.BytesIO(img_request.content))
            image_data.save(filename, optimize=True)
            skin_index += 1

create_folder_structure()
with open("mk1_links.json", "rt", encoding="utf-8") as mk1_links_file:
    mk1_links = json.loads(mk1_links_file.read())

with Pool() as pool:
    pool.map(save_character_costumes, mk1_links.keys())