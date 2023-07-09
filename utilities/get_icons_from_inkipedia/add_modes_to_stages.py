import json


file_path = "./spl3/base_files/config.json"
with open(file_path, 'rt', encoding='utf-8') as config_file:
    config_dict = json.loads(config_file.read())

mode_list_path = "./list_modes.json"
with open(mode_list_path, 'rt', encoding='utf-8') as mode_file:
    mode_dict = json.loads(mode_file.read())

salmon_list_path = "./salmon_run.json"
with open(salmon_list_path, 'rt', encoding='utf-8') as salmon_file:
    salmon_dict = json.loads(salmon_file.read())

stages_dict = config_dict.get("stage_to_codename")
new_stage_dict = {}

for key in stages_dict.keys():
    processed = False
    if "Salmon Run -" in key:
        new_stage_dict[key] = stages_dict[key]
        processed = True
    else:
        for mode in mode_list_path:
            if f"{mode} -" in key:
                new_stage_dict[key] = stages_dict[key]
                processed = True

    if not processed:
        for mode in mode_dict:
            new_key = f"{mode} - {key}"
            print(new_key)
            locale_data = {}
            for locale in stages_dict[key].get("locale").keys():
                locale_data[locale] = f"{mode_dict[mode][locale]} - {stages_dict[key]['locale'][locale]}"
            new_stage_dict[new_key] = {
                "locale": locale_data,
                "codename": stages_dict[key]["codename"]
            }

for key in salmon_dict.get("stages"):
    if f"Salmon Run - {key}" not in new_stage_dict.keys():
        new_key = f"{salmon_dict['mode']['name']} - {key}"
        locale_data = {}
        for locale in salmon_dict['stages'][key].keys():
            locale_data[locale] = f"{salmon_dict['mode']['locale'][locale]} - {salmon_dict['stages'][key][locale]}"
        new_stage_dict[new_key] = {
            "locale": locale_data,
            "codename": key.split(' ')[0].replace("'", '').lower()
        }

config_dict["stage_to_codename"] = new_stage_dict

with open(file_path, 'wt', encoding='utf-8') as config_file:
    config_file.write(json.dumps(config_dict, indent=2))