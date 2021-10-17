from os import link
import requests
from bs4 import BeautifulSoup as BS
import json
from pathlib import Path
import re
import zipfile

download_folder_name = "download"
Path(download_folder_name).mkdir(parents=True, exist_ok=True)

base_url = "https://www.eventhubs.com/news/2014/dec/31/hi-res-ultra-street-fighter-4-character-select-portraits-all-44-fighters/"

game_page = requests.get(base_url)
game_content = game_page.text
game_soup = BS(game_content, features="html.parser")

parse_tables = game_soup.findAll('a', href=True)
link_list = []
for tag in parse_tables:
    if ("https://www.eventhubs.com/images/2014/dec/31/character-select-ultra-street-fighter-4-portraits" in tag["href"]):
        link_list.append(f'{tag["href"]}')

print(len(link_list))

for link in link_list:
    portrait_page = requests.get(link)
    portrait_page_content = portrait_page.text
    portrait_page_soup = BS(portrait_page_content, features="html.parser")

    img_tables = portrait_page_soup.findAll('img')
    for tag in img_tables:
        if (tag["src"].endswith(".png")) and ("usf4art" in tag["src"]):
            filename = f'{download_folder_name}/{tag["src"].split("/")[-1]}'
            file_content = requests.get(tag["src"]).content
            with open(filename, 'wb') as f:
                f.write(file_content)
