import json
import glob
import pandas as pd

games_path = "../../games"
game_config_path_list = glob.glob(f"{games_path}/*/base_files/config.json")
ods_filename = "locale_data.ods"

title_dataframe = pd.read_excel(ods_filename, sheet_name="game_titles", index_col=0)

def process_config_section(section_name, config_section, game_codename):
    section_dataframe = pd.read_excel(ods_filename, sheet_name=f"{game_codename}.{section_name}", index_col=0)
    raw_data = section_dataframe.to_dict()
    for key in raw_data.keys():
        for locale in raw_data.get(key):
            if locale != "en" and raw_data.get(key).get(locale) and type(raw_data.get(key).get(locale)) == str:
                if config_section[key].get("locale"):
                    config_section[key]["locale"][locale] = raw_data.get(key).get(locale)
                else:
                    config_section[key]["locale"] = {locale: raw_data.get(key).get(locale)}
    return config_section

for game_config_path in game_config_path_list:
    game_codename = game_config_path.split("/")[-3]
    print("Processing", game_codename)
    with open(game_config_path, 'rt', encoding="utf-8") as game_config_file:
        game_config = json.loads(game_config_file.read())
    
    title_locale_data = title_dataframe.to_dict()[game_codename]
    for locale in title_locale_data.keys():
        if locale != "en" and title_locale_data.get(locale) and type(title_locale_data.get(locale)) == str:
            if game_config.get("locale"):
                if game_config.get("locale").get(locale):
                    game_config["locale"][locale]["name"] = title_locale_data.get(locale)
                else:
                    game_config["locale"][locale] = {"name": title_locale_data.get(locale)}
            else:
                game_config["locale"] = {locale: {"name": title_locale_data.get(locale)}}

    
    for section_name in ["character_to_codename", "stage_to_codename", "variant_to_codename"]:
        section_data = game_config.get(section_name)
        if section_data:
            section_data = process_config_section(section_name, section_data, game_codename)
            game_config[section_name] = section_data
    
    with open(game_config_path, 'wt', encoding="utf-8") as game_config_file:
        game_config_file.write(json.dumps(game_config, indent=2))