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

lang_list = ["ja", "ko", "zh-cmn-Hant", "zh-cmn-Hans","zh-Hant", "zh-Hans", "ru",
             "fr", "nl", "de", "it", "es", "fr-ca", "es-es", "es-mx", "fr-fr"]


def create_folder_structure():
    Path(root_path).mkdir(parents=True, exist_ok=True)
    # Path(full_path).mkdir(parents=True, exist_ok=True)
    Path(icon_path).mkdir(parents=True, exist_ok=True)
    Path(stage_path).mkdir(parents=True, exist_ok=True)
    Path(sub_path).mkdir(parents=True, exist_ok=True)
    Path(special_path).mkdir(parents=True, exist_ok=True)


def robust_request(link, timeout=30, recursion=30):
    try:
        response = requests.get(link, timeout=timeout)
        return_code = response.status_code
        if return_code != 200 and recursion > 0:
            return robust_request(link, timeout, recursion-1)
        else:
            return response
    except requests.exceptions.ConnectionError:
        return robust_request(link, timeout, recursion-1)


def generate_main_config_skeleton():
    description = "Base config to use this game."
    credits = ""
    version = "4.0"

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
            },
            "Brinewater Springs": {
                "codename": "brine"
            },
            "Flounder Heights": {
                "codename": "flounder"
            },
            "Um'ami Ruins": {
                "codename": "umami"
            },
            "Manta Maria": {
                "codename": "manta"
            },
            "Humpback Pump Track": {
                "codename": "track"
            },
            "Barnacle & Dime": {
                "codename": "track"
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


def write_configs(config_dict, sub_names, special_names):
    with open(f"{base_files_path}/config.json", "wt", encoding="utf-8") as f:
        f.write(json.dumps(config_dict, indent=2))

    version = config_dict["version"]

    icon_config_dict = {
        "prefix": "icon_",
        "postfix": "_",
        "type": ["icon"],
        "version": version,
        "uncropped_edge": [
            "u",
            "r",
            "d",
            "l"
        ]
    }

    with open(f"{icon_path}/config.json", "wt", encoding="utf-8") as f:
        f.write(json.dumps(icon_config_dict, indent=2))

    stage_config = {
        "name": "Stage Icons",
        "version": version,
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
        "version": version,
        "description": "Sub weapon icons",
        "prefix": "sub_",
        "postfix": "_",
        "type": [
            "sub"
        ],
        "credits": "Assets ripped from Inkipedia (https://splatoonwiki.org/)",
        "metadata": [sub_names],
        "uncropped_edge": [
            "u",
            "r",
            "d",
            "l"
        ]
    }

    with open(f"{sub_path}/config.json", "wt", encoding="utf-8") as f:
        f.write(json.dumps(sub_config, indent=2))

    special_config = {
        "name": "Special Icons",
        "version": version,
        "description": "Special icons",
        "prefix": "spe_",
        "postfix": "_",
        "type": [
            "special"
        ],
        "credits": "Assets ripped from Inkipedia (https://splatoonwiki.org/)",
        "metadata": [special_names],
        "uncropped_edge": [
            "u",
            "r",
            "d",
            "l"
        ]
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
sub_names = {
    "title": "Sub weapon",
    "locale": {
        "fr": "Arme secondaire"
    },
    "values": {}
}
special_names = {
    "title": "Special weapon",
    "locale": {
        "fr": "Arme spéciale"
    },
    "values": {}
}

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

weapon_index = 1
for weapon_name in weapon_list.keys():
    print("Processing weapon", weapon_index, "of", len(weapon_list), f"({weapon_name})")

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
        if lang == "zh-cmn-Hant" or lang == "zh-Hant":
            current_lang = "zh_TW"
        if lang == "zh-cmn-Hans" or lang == "zh-Hans":
            current_lang = "zh_CN"
        if lang == "fr-fr":
            current_lang = "fr"
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
                    main_config["character_to_codename"][weapon_name]["locale"][current_lang] = text_element.text.split("[")[
                        0]

    if (main_config["character_to_codename"][weapon_name]["locale"].get("zh_TW")) and not (main_config["character_to_codename"][weapon_name]["locale"].get("zh_CN")):
        main_config["character_to_codename"][weapon_name]["locale"]["zh_CN"] = chinese_converter.to_simplified(
            main_config["character_to_codename"][weapon_name]["locale"].get("zh_TW"))

    if (main_config["character_to_codename"][weapon_name]["locale"].get("zh_CN")) and not (main_config["character_to_codename"][weapon_name]["locale"].get("zh_TW")):
        main_config["character_to_codename"][weapon_name]["locale"]["zh_TW"] = chinese_converter.to_traditional(
            main_config["character_to_codename"][weapon_name]["locale"].get("zh_CN"))

    if (main_config["character_to_codename"][weapon_name]["locale"].get("fr_CA")) and not (main_config["character_to_codename"][weapon_name]["locale"].get("fr")):
        main_config["character_to_codename"][weapon_name]["locale"]["fr"] = main_config[
            "character_to_codename"][weapon_name]["locale"].get("fr_CA")

    if (main_config["character_to_codename"][weapon_name]["locale"].get("es_LA")) and not (main_config["character_to_codename"][weapon_name]["locale"].get("es")):
        main_config["character_to_codename"][weapon_name]["locale"]["es"] = main_config[
            "character_to_codename"][weapon_name]["locale"].get("es_LA")

    for line in weapon_body_lines:
        if f'title="{weapon_name}"' in str(line):
            images = line.findAll('img')
            for image_tag in images:
                if "Weapon Sub" in image_tag["alt"]:
                    sub_image_link = convert_weapon_thumb_link_to_image_link(
                        image_tag["src"])
                    sub_name = (image_tag["alt"].replace(
                        "S3 Weapon Sub ", "")).replace(" Flat.png", "")
                if "Weapon Special" in image_tag["alt"]:
                    special_image_link = convert_weapon_thumb_link_to_image_link(
                        image_tag["src"])
                    special_name = (image_tag["alt"].replace(
                        "S3 Weapon Special ", "")).replace(".png", "")
            break

    sub_filename = f"sub_{weapon_codename}_0.png"
    special_filename = f"spe_{weapon_codename}_0.png"
    with open(f"{sub_path}/{sub_filename}", "wb") as f:
        icon_file = robust_request(sub_image_link)
        f.write(icon_file.content)
    with open(f"{special_path}/{special_filename}", "wb") as f:
        icon_file = robust_request(special_image_link)
        f.write(icon_file.content)

    # Parsing sub names
    sub_names["values"][weapon_codename] = {"value": sub_name, "locale": {}}

    sub_wiki = f"https://splatoonwiki.org/wiki/{sub_name.replace(' ', '_')}"
    sub_wiki_page = robust_request(sub_wiki, timeout=30)
    sub_wiki_content = sub_wiki_page.text
    sub_wiki_soup = BS(sub_wiki_content, features="html.parser")

    for lang in lang_list:
        current_lang = lang
        if lang == "zh-cmn-Hant" or lang == "zh-Hant":
            current_lang = "zh_TW"
        if lang == "zh-cmn-Hans" or lang == "zh-Hans":
            current_lang = "zh_CN"
        if lang == "fr-fr":
            current_lang = "fr"
        if lang == "fr-ca":
            current_lang = "fr_CA"
        if lang == "es-es":
            current_lang = "es"
        if lang == "es-mx":
            current_lang = "es_LA"
        foreign_text = sub_wiki_soup.find_all(lang=lang)
        if foreign_text:
            for text_element in foreign_text:
                try:
                    if text_element["class"] == "interlanguage-link-target":
                        pass
                except:
                    sub_names["values"][weapon_codename]["locale"][current_lang] = text_element.text.split("[")[
                        0]
    if (sub_names["values"][weapon_codename]["locale"].get("zh_TW")) and not (sub_names["values"][weapon_codename]["locale"].get("zh_CN")):
        sub_names["values"][weapon_codename]["locale"]["zh_CN"] = chinese_converter.to_simplified(
            sub_names["values"][weapon_codename]["locale"].get("zh_TW"))

    if (sub_names["values"][weapon_codename]["locale"].get("zh_CN")) and not (sub_names["values"][weapon_codename]["locale"].get("zh_TW")):
        sub_names["values"][weapon_codename]["locale"]["zh_TW"] = chinese_converter.to_traditional(
            sub_names["values"][weapon_codename]["locale"].get("zh_CN"))

    if (sub_names["values"][weapon_codename]["locale"].get("fr_CA")) and not (sub_names["values"][weapon_codename]["locale"].get("fr")):
        sub_names["values"][weapon_codename]["locale"]["fr"] = sub_names["values"][weapon_codename]["locale"].get(
            "fr_CA")

    if (sub_names["values"][weapon_codename]["locale"].get("es_LA")) and not (sub_names["values"][weapon_codename]["locale"].get("es")):
        sub_names["values"][weapon_codename]["locale"]["es"] = sub_names["values"][weapon_codename]["locale"].get(
            "es_LA")

    # Parsing special names
    special_names["values"][weapon_codename] = {
        "value": special_name, "locale": {}}

    special_wiki = f"https://splatoonwiki.org/wiki/{special_name.replace(' ', '_')}"
    special_wiki_page = robust_request(special_wiki, timeout=30)
    special_wiki_content = special_wiki_page.text
    special_wiki_soup = BS(special_wiki_content, features="html.parser")

    for lang in lang_list:
        current_lang = lang
        if lang == "zh-cmn-Hant" or lang == "zh-Hant":
            current_lang = "zh_TW"
        if lang == "zh-cmn-Hans" or lang == "zh-Hans":
            current_lang = "zh_CN"
        if lang == "fr-fr":
            current_lang = "fr"
        if lang == "fr-ca":
            current_lang = "fr_CA"
        if lang == "es-es":
            current_lang = "es"
        if lang == "es-mx":
            current_lang = "es_LA"
        foreign_text = special_wiki_soup.find_all(lang=lang)
        if foreign_text:
            for text_element in foreign_text:
                try:
                    if text_element["class"] == "interlanguage-link-target":
                        pass
                except:
                    value_valid = True
                    for value in ["Thank you!", "Spritzig!", "¡Gracias!"]:
                        if value in text_element:
                            value_valid = False
                    if value_valid:
                        special_names["values"][weapon_codename]["locale"][current_lang] = text_element.text.split("[")[
                            0]
    if (special_names["values"][weapon_codename]["locale"].get("zh_TW")) and not (special_names["values"][weapon_codename]["locale"].get("zh_CN")):
        special_names["values"][weapon_codename]["locale"]["zh_CN"] = chinese_converter.to_simplified(
            special_names["values"][weapon_codename]["locale"].get("zh_TW"))

    if (special_names["values"][weapon_codename]["locale"].get("zh_CN")) and not (special_names["values"][weapon_codename]["locale"].get("zh_TW")):
        special_names["values"][weapon_codename]["locale"]["zh_TW"] = chinese_converter.to_traditional(
            special_names["values"][weapon_codename]["locale"].get("zh_CN"))

    if (special_names["values"][weapon_codename]["locale"].get("fr_CA")) and not (special_names["values"][weapon_codename]["locale"].get("fr")):
        special_names["values"][weapon_codename]["locale"]["fr"] = special_names["values"][weapon_codename]["locale"].get(
            "fr_CA")

    if (special_names["values"][weapon_codename]["locale"].get("es_LA")) and not (special_names["values"][weapon_codename]["locale"].get("es")):
        special_names["values"][weapon_codename]["locale"]["es"] = special_names["values"][weapon_codename]["locale"].get(
            "es_LA")

    weapon_index += 1

    # print(json.dumps(sub_names["values"][weapon_codename], indent=2))
    # print(json.dumps(special_names["values"][weapon_codename], indent=2))

for stage_name in main_config["stage_to_codename"]:
    main_config["stage_to_codename"][stage_name]["locale"] = {}

    weapon_wiki = f"https://splatoonwiki.org/wiki/{stage_name.replace(' ', '_')}"
    weapon_wiki_page = robust_request(weapon_wiki, timeout=30)
    weapon_wiki_content = weapon_wiki_page.text
    weapon_wiki_soup = BS(weapon_wiki_content, features="html.parser")

    for lang in lang_list:
        current_lang = lang
        if lang == "zh-cmn-Hant" or lang == "zh-Hant":
            current_lang = "zh_TW"
        if lang == "zh-cmn-Hans" or lang == "zh-Hans":
            current_lang = "zh_CN"
        if lang == "fr-fr":
            current_lang = "fr"
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
                    main_config["stage_to_codename"][stage_name]["locale"][current_lang] = text_element.text.split("[")[
                        0]

    if (main_config["stage_to_codename"][stage_name]["locale"].get("zh_TW")) and not (main_config["stage_to_codename"][stage_name]["locale"].get("zh_CN")):
        main_config["stage_to_codename"][stage_name]["locale"]["zh_CN"] = chinese_converter.to_simplified(
            main_config["stage_to_codename"][stage_name]["locale"].get("zh_TW"))

    if (main_config["stage_to_codename"][stage_name]["locale"].get("zh_CN")) and not (main_config["stage_to_codename"][stage_name]["locale"].get("zh_TW")):
        main_config["stage_to_codename"][stage_name]["locale"]["zh_TW"] = chinese_converter.to_traditional(
            main_config["stage_to_codename"][stage_name]["locale"].get("zh_CN"))

    if (main_config["stage_to_codename"][stage_name]["locale"].get("fr_CA")) and not (main_config["stage_to_codename"][stage_name]["locale"].get("fr")):
        main_config["stage_to_codename"][stage_name]["locale"]["fr"] = main_config["stage_to_codename"][stage_name]["locale"].get(
            "fr_CA")

    if (main_config["stage_to_codename"][stage_name]["locale"].get("es_LA")) and not (main_config["stage_to_codename"][stage_name]["locale"].get("es")):
        main_config["stage_to_codename"][stage_name]["locale"]["es"] = main_config["stage_to_codename"][stage_name]["locale"].get(
            "es_LA")

write_configs(main_config, sub_names, special_names)
