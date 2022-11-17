import requests
from bs4 import BeautifulSoup as BS
import json
from pathlib import Path
from copy import deepcopy

directory = "serebii"
form_directory = f"{directory}/paldeaform"
new_directory = f"{directory}/new"
pokedex_filename = f"{directory}/dex.json"

Path(form_directory).mkdir(parents=True, exist_ok=True)
Path(new_directory).mkdir(parents=True, exist_ok=True)

form_url = "https://serebii.net/scarletviolet/paldeanforms.shtml"
new_url = "https://serebii.net/scarletviolet/pokemon.shtml"


def robust_request(link, timeout=30):
    return_code = 404
    while return_code != 200:
        try:
            response = requests.get(link, timeout=timeout)
            return_code = response.status_code
        except requests.exceptions.ConnectionError:
            return robust_request(link)
    return response


def download_forms():
    form_page = robust_request(form_url, timeout=30)
    content = form_page.text
    soup = BS(content, features="html.parser")
    tables = soup.findAll("table")

    form_table = None

    for table in tables:
        if "Tauros" in table.get_text():
            form_table = table

    if not form_table:
        exit(2)

    table_rows = form_table.findAll("tr")
    for row in table_rows:
        dex_number = None
        if "#" in row.get_text():
            elements = row.findAll("td")
            for element in elements:
                if "#" in element.get_text():
                    dex_number: str = element.get_text()
                    dex_number = dex_number.strip().removeprefix("#")
                #   print(dex_number)
                    icon_url = f"https://serebii.net/scarletviolet/pokemon/{dex_number}-p.png"
                    icon_filename = f"{form_directory}/icon_{dex_number}_1.png"
                    icon_file = robust_request(icon_url)
                    with open(icon_filename, 'wb') as f:
                        f.write(icon_file.content)


def download_new():
    new_page = robust_request(new_url, timeout=30)
    content = new_page.text
    soup = BS(content, features="html.parser")
    tables = soup.findAll("table")

    form_table = None

    for table in tables:
        if "Toedscruel" in table.get_text():
            form_table = table

    if not form_table:
        exit(2)

    table_rows = form_table.findAll("tr")
    pokedex = {}
    for row in table_rows:
        dex_number = None
        # print(row)

        if "/scarletviolet/pokemon/" in str(row) and "/abilitydex/" in str(row):
            elements = row.findAll("img")
            index = 0
            for element in elements:
                index+=1
                if "/scarletviolet/pokemon/" in element["src"]:
                    dex_number: str = element["src"]
                    dex_number = dex_number.strip().removeprefix("/scarletviolet/pokemon/").removesuffix(".png")
                    print(dex_number)
                    icon_url = f"https://serebii.net/scarletviolet/pokemon/{dex_number}.png"
                    icon_filename = f"{new_directory}/icon_{dex_number}_0.png"
                    icon_file = robust_request(icon_url)
                    with open(icon_filename, 'wb') as f:
                        f.write(icon_file.content)

            elements = row.findAll("a")
            pokemon_name = str(elements[1])
            if "<br/>" in pokemon_name:
                pokemon_name = pokemon_name.split("<br/>")[0]
                pokemon_name = pokemon_name.split('>')[-1]
            else:
                pokemon_name = elements[1].get_text().strip()

            if pokemon_name not in pokedex.keys():
                pokedex[pokemon_name] = {"codename": str(dex_number)}

    with open(pokedex_filename, 'wt') as f:
        f.write(json.dumps(pokedex, indent=2))

download_forms()
download_new()
