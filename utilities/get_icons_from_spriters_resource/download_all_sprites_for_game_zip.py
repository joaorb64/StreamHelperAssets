import requests
from bs4 import BeautifulSoup as BS
import json
from pathlib import Path
import re
import zipfile

download_folder_name = "download"
Path(download_folder_name).mkdir(parents=True, exist_ok=True)

base_url = "https://www.spriters-resource.com/xbox_360/ultimatemarvelvscapcom3/"

game_page = requests.get(base_url)
game_content = game_page.text
game_soup = BS(game_content, features="html.parser")

parse_tables = game_soup.findAll('a', href=True)
link_list = []
for tag in parse_tables:
    if ('class="iconheadertext"' in str(tag)) and ("xbox_360/ultimatemarvelvscapcom3/sheet/" in tag["href"]):
        link_list.append(f'https://www.spriters-resource.com{tag["href"]}')

filenames = []

for link in link_list:
    split = link.split('/')
    while not split[-1]:
        split.pop()
    id = split[-1]

    sprite_sheet_page = requests.get(link)
    sprite_sheet_content = sprite_sheet_page.text
    sprite_sheet_soup = BS(sprite_sheet_content, features="html.parser")
    sprite_sheet_tags = sprite_sheet_soup.findAll('a', href=True)
    for tag in sprite_sheet_tags:
        if ("download" in tag["href"]) and (id in tag["href"]):
            link = f'https://www.spriters-resource.com{tag["href"]}'
            download_split = link.split('/')
            while not download_split[-1]:
                download_split.pop()
            filename = f"{download_folder_name}/{download_split[-1]}.zip"
            file_content = requests.get(link).content
            with open(filename, 'wb') as f:
                f.write(file_content)
            with zipfile.ZipFile(filename, 'r') as zip_ref:
                zip_ref.extractall(download_folder_name)

print(filenames)