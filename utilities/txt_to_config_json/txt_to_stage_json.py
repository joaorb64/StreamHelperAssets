import json
from pathlib import Path

game_id = 16388
stage_list_filename = "stages_list.txt"

with open(f"stage.json", 'wt') as config_file:
    description = "Base config to use this game."
    credits = ''
    version = "1.0"

    config_dict: dict = {
        "stage_to_codename": {}
    }

    with open(f"{stage_list_filename}", 'rt', encoding='utf-8') as stage_list:
        for stage_name in stage_list:
            stage_name = stage_name.strip()
            if stage_name:
                codename = stage_name
                for str_character in " &.(?!;/:%\\|-_\"'~@[{}]":
                    codename = codename.replace(str_character, "")
                config_dict["stage_to_codename"][stage_name] = {
                    "codename": codename
                }

    config_file_content = json.dumps(config_dict, indent=2, sort_keys=False)
    config_file.write(config_file_content)
