import requests
from bs4 import BeautifulSoup as BS
import json
from pathlib import Path
from copy import deepcopy
import re


main_path = "../../games/pkmn"
main_config_path = f"{main_path}/base_files/config.json"
variant_folder_path = f"{main_path}/variant_icon"
variant_config_path = f"{variant_folder_path}/config.json"
prefix = "file_"
postfix = ""
file_format = ".png"

Path(variant_folder_path).mkdir(parents=True, exist_ok=True)

base_page_url = "https://serebii.net/itemdex/"
base_page = requests.get(base_page_url)
base_page_content = base_page.text
base_page_soup = BS(base_page_content, features="html.parser")

tables = base_page_soup.findAll("table")

menus = []

for table in tables:
    form_list = table.findAll("form")
    for form in form_list:
        if form.get("name") in ["pokeball", "recovery", "holditem", "evolution", "key", "misc", "battle", "mail", "berry"]:
            menus.append(form)

item_list = {}

for form in menus:
    option_list = form.findAll("option")
    for option in option_list:
        if "/list/" not in option.get("value"):
            item_name = option.text
            print("Processing", item_name)
            item_img_url = None
            item_page_url = "https://serebii.net" + option.get("value")
            item_page = requests.get(item_page_url)
            if item_page.status_code == 200:
                item_page_content = item_page.text
                item_page_soup = BS(item_page_content, features="html.parser")

                dextables = item_page_soup.findAll("table", {"class": "dextable"})
                for dextable in dextables:
                    dextable_rows = dextable.findAll("tr")
                    for row in dextable_rows:
                        if "Sprites" in row.text:
                            dextable_imgs = dextable.findAll('img')
                            for dextable_img in dextable_imgs:
                                if "/itemdex/sprites" in dextable_img.get("src"):
                                    item_img_url = "https://serebii.net" + dextable_img.get("src")
                                    print(item_img_url)
                            break

            item_list[item_name] = item_img_url

variant_list = {}

for item_name in item_list:
    item_codename = re.sub(r'[^a-zA-Z0-9]', '_', item_name)
    variant_list[item_name] = {"codename": item_codename}
    if item_list.get(item_name):
        item_image_page = requests.get(item_list.get(item_name))
        image_filename = f"{variant_folder_path}/{prefix}{item_codename}{postfix}{file_format}"
        with open(image_filename, 'wb') as f:
            f.write(item_image_page.content)

variant_config = {
    "name": "Item Icons",
    "version": "1.0",
    "description": "Item icons\nRequires TSH 5.92 or higher to be used",
    "prefix": prefix,
    "postfix": postfix,
    "type": [
        "variant_icon"
    ],
    "credits": f"Ripped from {base_page_url}"
}

with open(variant_config_path, "wt") as variant_config_file:
    variant_config_file.write(json.dumps(variant_config, indent=2))

with open(main_config_path, 'rt') as main_config_file:
    main_config = json.loads(main_config_file.read())

main_config["variant_to_codename"] = variant_list

with open(main_config_path, 'wt') as main_config_file:
    main_config_file.write(json.dumps(main_config, indent=2))
