import json
from pathlib import Path
import chinese_converter

root_path = "../../games/ddnd"
base_files_path = f"{root_path}/base_files"
config_path = f"{base_files_path}/config.json"

with open(config_path, 'rt', encoding="utf-8") as config_file:
    config_dict = json.loads(config_file.read())

for character in config_dict["character_to_codename"].keys():
    simplified_name = config_dict["character_to_codename"][character]["locale"].get("zh_CN")
    if simplified_name != chinese_converter.to_simplified(simplified_name):
        simplified_name = chinese_converter.to_simplified(simplified_name)
    config_dict["character_to_codename"][character]["locale"]["zh_CN"] = simplified_name
    traditional_name = chinese_converter.to_traditional(simplified_name)
    if not config_dict["character_to_codename"][character]["locale"].get("zh_TW"):
        config_dict["character_to_codename"][character]["locale"]["zh_TW"] = traditional_name
    else:
        traditional_name = config_dict["character_to_codename"][character]["locale"]["zh_TW"]
    print(character, simplified_name, traditional_name)

with open(config_path, 'wt', encoding="utf-8") as config_file:
    config_file.write(json.dumps(config_dict, indent=2))
