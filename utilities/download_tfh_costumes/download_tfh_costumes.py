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
import re

sys.setrecursionlimit(100)

base_url = "https://mizuumi.wiki/w/Them%27s_Fightin%27_Herds"

root_path = "../../games/tfh"
costumes = f"{root_path}/costume"
main_config_path = f"{root_path}/base_files/config.json"
with open(main_config_path, 'rt', encoding="utf-8") as f:
    main_config = json.loads(f.read())


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

def get_all_character_page_links():
    character_pages = {}
    for character_name in main_config.get("character_to_codename", {}).keys():
        character_url = f"{base_url}/{character_name}"
        print(character_url)
        character_response = robust_request(character_url)
        assert character_response.status_code == 200
        character_pages[character_name] = character_response
    return character_pages

def get_original_image_url(small_image_uri):
    "/images/thumb/f/f8/TFH-Baihe-1.png/195px-TFH-Baihe-1.png"
    uri_regex = "\/images\/thumb\/(.*)\/(.*)\/(.*\.png)\/"
    parsed_uri = re.search(uri_regex, small_image_uri)
    image_url = f"https://mizuumi.wiki/images/{parsed_uri.group(1)}/{parsed_uri.group(2)}/{parsed_uri.group(3)}"
    return(image_url)

def parse_character_page_link(character_page):

    content = character_page.text
    soup = BS(content, features="html.parser")

    # Find the Colors header
    headers = soup.findAll('div', {"class": "mw-heading mw-heading2"})
    color_header = None
    for header in headers:
        if header.get_text() == "Colors":
            color_header = header

    # Find the table right after that
    divs = color_header.find_all_next("div")
    color_div = None
    for div in divs:
        if ".png" in str(div):
            color_div = div
            break

    # Extract all images and skin names in order
    color_list = []
    color_spans = color_div.findAll('span')
    for i in range(len(color_spans)):
        color_span = color_spans[i]
        color_span_divs = color_span.findAll('div')
        if color_span_divs:
            color_span_header = color_span_divs[0]
            color_name = color_span_header.get_text()
            # Fixes
            color_name = color_name.replace("( ", "(")
            color_name = color_name.replace(" )", ")")
            print(color_name)
            color_span_imgs = color_span.findAll("img")
            color_span_img = color_span_imgs[0]
            color_uri = color_span_img["src"]
            color_url = get_original_image_url(color_uri)

            color_list.append(
                {
                    "name": color_name,
                    "url": color_url
                }
            )

    return(color_list)

character_pages = get_all_character_page_links()

costume_config = {
  "name": "Colors",
  "description": "Alternate colors for each character",
  "prefix": "file_",
  "postfix": "_",
  "type": [
    "costume"
  ],
  "credits": f"Ripped from {base_url}",
  "version": "1.0"
}

for character_name in character_pages.keys():
    character_codename = main_config["character_to_codename"][character_name]["codename"]
    character_color_images = parse_character_page_link(character_pages[character_name])
    color_names_in_main_config = {}
    for i in range(len(character_color_images)):
        color_names_in_main_config[str(i)] = {"name": character_color_images[i]["name"]}
        image_url = character_color_images[i]["url"]
        image_response = robust_request(image_url)
        assert image_response.status_code == 200, f"Could not find image at url {image_url}, response {image_response.status_code}"
        image_filename = f'{costume_config["prefix"]}{character_codename}{costume_config["postfix"]}{i:02}.png'
        print(image_filename)
        image_path = f"{costumes}/{image_filename}"
        with open(image_path, 'wb') as f:
            f.write(image_response.content)
    
    main_config["character_to_codename"][character_name]["skin_name"] = color_names_in_main_config

with open(main_config_path, "wt", encoding="utf-8") as f:
    f.write(json.dumps(main_config, indent=2))

with open(f"{costumes}/config.json", "wt", encoding="utf-8") as f:
    f.write(json.dumps(costume_config, indent=2))