import requests
from bs4 import BeautifulSoup as BS
import json
from copy import deepcopy

def robust_request(link, timeout=30):
    return_code = 404
    while return_code != 200:
        try:
            response = requests.get(link, timeout=timeout)
            return_code = response.status_code
        except requests.exceptions.ConnectionError:
            return robust_request(link)
    return response

list_games = ["pkmn", "punite", "pcombat", "pokkendx", "ssb64", "ssbb", "ssbu", "ssbm", "ssbwiiu", "pplus"]
credit = "Breton Pokémon names by Anthony Guéchoum (Extracted from https://web.archive.org/web/20240720193925/http://brezhonadur.com/pokedex.php)"

dex_url = "https://web.archive.org/web/20240720193925/http://brezhonadur.com/pokedex.php"
dex_page = robust_request(dex_url, timeout=30)
dex_content = dex_page.text
dex_soup = BS(dex_content, features="html.parser")

pokemon_divs = dex_soup.findAll("div", {"class": "grid-element filter-selected"})
for pokemon_div in pokemon_divs:
    element = pokemon_div.findAll("a")
    id, name_br, name_fr = element[0]["data-id"], element[0].text, element[0]["data-fr"]

    if int(id) == 29: # Fix for Nidoran
        name_br = name_br + "♀"
    if int(id) == 32:
        name_br = name_br + "♂"

    print(id, name_br, name_fr)

    for game in list_games:
        config_path = f"../../games/{game}/base_files/config.json"
        with open(config_path, "rt", encoding="utf-8") as config_file:
            config = json.loads(config_file.read())
        changed = False
        for name_en in config["character_to_codename"].keys():
            if config["character_to_codename"][name_en].get("locale") and (name_fr == config["character_to_codename"][name_en].get("locale", {}).get("fr")
                                                                           or (id in config["character_to_codename"][name_en]["codename"] and (len(config["character_to_codename"][name_en]["codename"]) <= 3 or "-" in config["character_to_codename"][name_en]["codename"]))):
                config["character_to_codename"][name_en]["locale"]["br"] = name_br
                changed = True
        if changed and not (credit in config.get("credits", "")):
            if config.get("credits"):
                config["credits"] = config["credits"] + "\n" + credit
            else:
                config["credits"] = deepcopy(credit)
        if changed:
            with open(config_path, "wt", encoding="utf-8") as config_file:
                config_file.write(json.dumps(config, indent=2))
