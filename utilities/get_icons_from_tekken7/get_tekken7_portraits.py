from os import link
import requests
from bs4 import BeautifulSoup as BS
import json
from pathlib import Path
import re
import zipfile

download_folder_name = "download"
Path(download_folder_name).mkdir(parents=True, exist_ok=True)

base_url = "https://tk7.tekken.com"

# You'll have to download the page from https://tk7.tekken.com/fighters to this directory
# use Firefox if Chrome doesn't download the full page

game_page = open("./Tekken 7 - The Best Fights Are Personal.html").read()
game_content = game_page
game_soup = BS(game_content, features="html.parser")

parse_images = game_soup.findAll('figure')
link_list = []
for tag in parse_images:
    if ("/assets/images/fighters-final/" in tag["bn-background"]):
        link_list.append(f'{base_url}{tag["bn-background"]}')

print(len(link_list))

for link in link_list:
    print(link)

    # Format: https://tk7.tekken.com/assets/images/fighters-final/raven-standard/thumbnail-headshot.png
    # Remove last 9 digits to remove "-final"
    filename = f'{download_folder_name}/{link.split("/")[-2][0:-9]}'
    file_content = requests.get(link).content
    with open(filename, 'wb') as f:
        f.write(file_content)
