import requests
from bs4 import BeautifulSoup as BS
import json
from pathlib import Path
import sys
import chinese_converter

sys.setrecursionlimit(100)

root_path = "spl3"
base_files_path = f"{root_path}/base_files"
full_path = f"{root_path}/full"
icon_path = f"{base_files_path}/icon"
stage_path = f"{root_path}/stage_icon"
sub_path = f"{root_path}/sub"
special_path = f"{root_path}/special"

lang_list = ["ja", "ko", "zh-cmn-Hant", "zh-cmn-Hans", "ru",
             "fr", "nl", "de", "it", "es", "fr-ca", "es-es", "es-mx"]


def create_folder_structure():
    Path(root_path).mkdir(parents=True, exist_ok=True)
    # Path(full_path).mkdir(parents=True, exist_ok=True)
    Path(icon_path).mkdir(parents=True, exist_ok=True)
    Path(stage_path).mkdir(parents=True, exist_ok=True)
    Path(sub_path).mkdir(parents=True, exist_ok=True)
    Path(special_path).mkdir(parents=True, exist_ok=True)


def robust_request(link, timeout=30):
    return_code = 404
    while return_code != 200:
        try:
            response = requests.get(link, timeout=timeout)
            return_code = response.status_code
        except requests.exceptions.ConnectionError:
            return robust_request(link)
    return response


def generate_main_config_skeleton():
    description = "Base config to use this game."
    credits = ""
    version = "1.0"

    game_id = 36202

    with open(
        f"../download_smashgg/game_data.json", "rt", encoding="utf-8"
    ) as game_data_file:
        game_data = json.loads(game_data_file.read())
    found = False
    for game in game_data:
        if game.get("smashgg_id") == game_id:
            game_name = game.get("name")
            challonge_id = game.get("challonge_id")
            found = True

    if not found:
        print("Game not found")
        exit(1)

    config_dict: dict = {
        "name": str(game_name),
        "smashgg_game_id": game_id,
        "challonge_game_id": challonge_id,
        "character_to_codename": {},
        "stage_to_codename": {
            "Scorch Gorge": {
                "codename": "scorch"
            },
            "Eeltail Alley": {
                "codename": "eeltail"
            },
            "Hagglefish Market": {
                "codename": "hagglefish"
            },
            "Undertow Spillway": {
                "codename": "undertow"
            },
            "Mincemeat Metalworks": {
                "codename": "metalworks"
            },
            "Hammerhead Bridge": {
                "codename": "hammerhead"
            },
            "Museum d'Alfonsino": {
                "codename": "alfonsino"
            },
            "Mahi-Mahi Resort": {
                "codename": "mahi"
            },
            "Inkblot Art Academy": {
                "codename": "inkblot"
            },
            "Sturgeon Shipyard": {
                "codename": "sturgeon"
            },
            "MakoMart": {
                "codename": "mako"
            },
            "Wahoo World": {
                "codename": "wahoo"
            }
        },
        "version": version,
        "description": str(description),
        "credits": str(credits),
        "locale": {
            "ja": {
                "name": "スプラトゥーン3"
            },
            "zh_CN": {
                "name": "斯普拉遁3"
            },
            "zh_TW": {
                "name": "斯普拉遁3"
            },
            "ko": {
                "name": "스플래툰 3"
            }
        }
    }

    return config_dict


def convert_weapon_thumb_link_to_image_link(weapon_link):
    weapon_link = f'https:{weapon_link}'
    weapon_link = weapon_link.replace(weapon_link.split('/')[-1], "")
    weapon_link = weapon_link.replace("/thumb", "")
    weapon_link = weapon_link.strip("/")
    return(weapon_link)


def write_configs(config_dict):
    with open(f"{base_files_path}/config.json", "wt", encoding="utf-8") as f:
        f.write(json.dumps(config_dict, indent=2))

    version = config_dict["version"]

    icon_config_dict = {
        "prefix": "icon_",
        "postfix": "_",
        "type": ["icon"],
        "version": version,
    }

    with open(f"{icon_path}/config.json", "wt", encoding="utf-8") as f:
        f.write(json.dumps(icon_config_dict, indent=2))

    stage_config = {
        "name": "Stage Icons",
        "version": "1.0",
        "description": "Stage icons",
        "prefix": "stage_",
        "postfix": "",
        "type": [
            "stage_icon"
        ]
    }

    with open(f"{stage_path}/config.json", "wt", encoding="utf-8") as f:
        f.write(json.dumps(stage_config, indent=2))

    sub_config = {
        "name": "Sub Icons",
        "version": "1.0",
        "description": "Sub weapon icons",
        "prefix": "sub_",
        "postfix": "",
        "type": [
            "sub"
        ],
        "credits": "Assets ripped from Inkipedia (https://splatoonwiki.org/)"
    }

    with open(f"{sub_path}/config.json", "wt", encoding="utf-8") as f:
        f.write(json.dumps(sub_config, indent=2))

    special_config = {
        "name": "Special Icons",
        "version": "1.0",
        "description": "Special icons",
        "prefix": "spe_",
        "postfix": "",
        "type": [
            "special"
        ],
        "credits": "Assets ripped from Inkipedia (https://splatoonwiki.org/)"
    }

    with open(f"{special_path}/config.json", "wt", encoding="utf-8") as f:
        f.write(json.dumps(special_config, indent=2))


create_folder_structure()

weapon_page = (
    "https://splatoonwiki.org/wiki/List_of_weapons_in_Splatoon_3"
)
weapon_page = robust_request(weapon_page, timeout=30)
weapon_content = weapon_page.text
weapon_soup = BS(weapon_content, features="html.parser")
weapon_tables = weapon_soup.findAll("table")
weapon_body_tag = None
for table in weapon_tables:
    tbody_list = table.findAll('tbody')
    for tbody in tbody_list:
        if ".52 Gal" in str(tbody):
            weapon_body_tag = tbody
            break
    if weapon_body_tag:
        break

weapon_body_images = weapon_body_tag.findAll('img')

weapon_list = {}

for image_tag in weapon_body_images:
    if "S3_Weapon_Main" in image_tag["src"]:
        weapon_name = image_tag["alt"]
        weapon_name = weapon_name.replace("S3 Weapon Main ", "")
        weapon_name = weapon_name.replace(" Flat.png", "")
        weapon_list[weapon_name] = {
            "main_image": convert_weapon_thumb_link_to_image_link(image_tag["src"])}

print(json.dumps(weapon_list, indent=2))
print(len(weapon_list))

main_config = generate_main_config_skeleton()

weapon_body_lines = weapon_body_tag.findAll('tr')

# print(weapon_body_lines)

for weapon_name in weapon_list.keys():
    sub_image_link, special_image_link = None, None
    icon_url = weapon_list[weapon_name]["main_image"]
    weapon_codename = weapon_name.replace(".", "")
    weapon_codename = weapon_codename.replace(" ", "")
    weapon_codename = weapon_codename.replace("-", "")
    icon_filename = f"icon_{weapon_codename}_0.png"
    with open(f"{icon_path}/{icon_filename}", "wb") as f:
        icon_file = robust_request(icon_url)
        f.write(icon_file.content)
    main_config["character_to_codename"][weapon_name] = {
        "codename": weapon_codename}
    main_config["character_to_codename"][weapon_name]["locale"] = {}

    weapon_wiki = f"https://splatoonwiki.org/wiki/{weapon_name.replace(' ', '_')}"
    weapon_wiki_page = robust_request(weapon_wiki, timeout=30)
    weapon_wiki_content = weapon_wiki_page.text
    weapon_wiki_soup = BS(weapon_wiki_content, features="html.parser")

    for lang in lang_list:
        current_lang = lang
        if lang == "zh-cmn-Hant":
            current_lang = "zh_TW"
        if lang == "zh-cmn-Hans":
            current_lang = "zh_CN"
        if lang == "fr-fr":
            current_lang = "fr_FR"
        if lang == "fr-ca":
            current_lang = "fr_CA"
        if lang == "es-es":
            current_lang = "es"
        if lang == "es-mx":
            current_lang = "es_LA"
        foreign_text = weapon_wiki_soup.find_all(lang=lang)
        if foreign_text:
            for text_element in foreign_text:
                try:
                    if text_element["class"] == "interlanguage-link-target":
                        pass
                except:
                    main_config["character_to_codename"][weapon_name]["locale"][current_lang] = text_element.text.split("[")[0]

    if (main_config["character_to_codename"][weapon_name]["locale"].get("zh_TW")) and not (main_config["character_to_codename"][weapon_name]["locale"].get("zh_CN")):
        main_config["character_to_codename"][weapon_name]["locale"]["zh_CN"] = chinese_converter.to_simplified(main_config["character_to_codename"][weapon_name]["locale"].get("zh_TW"))

    if (main_config["character_to_codename"][weapon_name]["locale"].get("zh_CN")) and not (main_config["character_to_codename"][weapon_name]["locale"].get("zh_TW")):
        main_config["character_to_codename"][weapon_name]["locale"]["zh_TW"] = chinese_converter.to_traditional(main_config["character_to_codename"][weapon_name]["locale"].get("zh_CN"))


    for line in weapon_body_lines:
        if f'title="{weapon_name}"' in str(line):
            images = line.findAll('img')
            for image_tag in images:
                if "Weapon Sub" in image_tag["alt"]:
                    sub_image_link = convert_weapon_thumb_link_to_image_link(
                        image_tag["src"])
                if "Weapon Special" in image_tag["alt"]:
                    special_image_link = convert_weapon_thumb_link_to_image_link(
                        image_tag["src"])
            break

    sub_filename = f"sub_{weapon_codename}_0.png"
    special_filename = f"spe_{weapon_codename}_0.png"
    with open(f"{sub_path}/{sub_filename}", "wb") as f:
        icon_file = robust_request(sub_image_link)
        f.write(icon_file.content)
    with open(f"{special_path}/{special_filename}", "wb") as f:
        icon_file = robust_request(special_image_link)
        f.write(icon_file.content)

for stage_name in main_config["stage_to_codename"]:
    main_config["stage_to_codename"][stage_name]["locale"] = {}

    weapon_wiki = f"https://splatoonwiki.org/wiki/{stage_name.replace(' ', '_')}"
    weapon_wiki_page = robust_request(weapon_wiki, timeout=30)
    weapon_wiki_content = weapon_wiki_page.text
    weapon_wiki_soup = BS(weapon_wiki_content, features="html.parser")

    for lang in lang_list:
        current_lang = lang
        if lang == "zh-cmn-Hant":
            current_lang = "zh_TW"
        if lang == "zh-cmn-Hans":
            current_lang = "zh_CN"
        if lang == "fr-fr":
            current_lang = "fr_FR"
        if lang == "fr-ca":
            current_lang = "fr_CA"
        if lang == "es-es":
            current_lang = "es"
        if lang == "es-mx":
            current_lang = "es_LA"
        foreign_text = weapon_wiki_soup.find_all(lang=lang)
        if foreign_text:
            for text_element in foreign_text:
                try:
                    if text_element["class"] == "interlanguage-link-target":
                        pass
                except:
                    main_config["stage_to_codename"][stage_name]["locale"][current_lang] = text_element.text.split("[")[0]

    if (main_config["stage_to_codename"][stage_name]["locale"].get("zh_TW")) and not (main_config["stage_to_codename"][stage_name]["locale"].get("zh_CN")):
        main_config["stage_to_codename"][stage_name]["locale"]["zh_CN"] = chinese_converter.to_simplified(main_config["stage_to_codename"][stage_name]["locale"].get("zh_TW"))

    if (main_config["stage_to_codename"][stage_name]["locale"].get("zh_CN")) and not (main_config["stage_to_codename"][stage_name]["locale"].get("zh_TW")):
        main_config["stage_to_codename"][stage_name]["locale"]["zh_TW"] = chinese_converter.to_traditional(main_config["stage_to_codename"][stage_name]["locale"].get("zh_CN"))

write_configs(main_config)
