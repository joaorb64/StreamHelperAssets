import json
import glob
import pandas as pd

games_path = "../../games"
game_config_path_list = glob.glob(f"{games_path}/*/base_files/config.json")
ods_data_unformatted = {
    "game_titles" : {}
}
ods_filename = "locale_data.ods"

def process_config_section(config_section):
    if config_section:
        section_result = {}

        for name in config_section.keys():
            locale = config_section.get(name).get("locale", {})
            section_result[name] = locale
        
        return section_result
    else:
        return None

for game_config_path in game_config_path_list:
    game_codename = game_config_path.split("/")[-3]
    print("Processing", game_codename)
    with open(game_config_path, 'rt', encoding="utf-8") as game_config_file:
        game_config = json.loads(game_config_file.read())
    
    game_name = game_config["name"]
    game_locale = game_config.get("locale", {})
    game_title_dict = {"en": game_name}
    for locale in game_locale:
        if game_locale.get(locale).get("name"):
            game_title_dict[locale] = game_locale.get(locale).get("name")
    
    ods_data_unformatted["game_titles"][game_codename] = game_title_dict

    for section_name in ["character_to_codename", "stage_to_codename", "variant_to_codename"]:
        section_ods_name = f"{game_codename}.{section_name}"
        section_data = process_config_section(game_config.get(section_name))
        if section_data:
            ods_data_unformatted[section_ods_name] = section_data


with pd.ExcelWriter(ods_filename) as excel_writer:
    for sheet_name in ods_data_unformatted:
        df = pd.DataFrame.from_dict(ods_data_unformatted[sheet_name])
        df.to_excel(excel_writer, sheet_name=sheet_name)
