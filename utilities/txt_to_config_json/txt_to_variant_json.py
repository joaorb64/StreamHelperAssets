import json
from pathlib import Path

game_id = 9973
variant_list_filename = "variants_list.txt"

with open(f"variant.json", 'wt') as config_file:
    description = "Base config to use this game."
    credits = ''
    version = "1.0"

    config_dict: dict = {
        "variant_to_codename": {}
    }

    with open(f"{variant_list_filename}", 'rt', encoding='utf-8') as variant_list:
        for variant_name in variant_list:
            variant_name = variant_name.strip()
            if variant_name:
                codename = variant_name + "V"
                for str_character in " &.()?!;/:%\\|-_\"'~@[{}]":
                    codename = codename.replace(str_character, "")
                config_dict["variant_to_codename"][variant_name] = {
                    "codename": codename
                }
                Path("variant_icon").mkdir(parents=True, exist_ok=True)
                with open(f"variant_icon/file_{codename}.png", "wb") as blank_variant_file:
                    blank_variant_file.write(bytearray())

    config_file_content = json.dumps(config_dict, indent=2, sort_keys=False)
    config_file.write(config_file_content)
