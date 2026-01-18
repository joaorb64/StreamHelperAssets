from PIL import Image
import json
import shutil
import glob

list_characters = glob.glob("./input/*/")
for i in range(len(list_characters)):
    list_characters[i] = list_characters[i].split("/")[-2]
portrait_scaling = 4

print(list_characters)

root_path = f"../../games/roa"
main_config_path = f"{root_path}/base_files/config.json"
with open(main_config_path, "rt", encoding="utf-8") as main_config_file:
    main_config = json.loads(main_config_file.read())

portrait_path = f"{root_path}/costume"
portrait_config_path = f"{portrait_path}/config.json"
with open(portrait_config_path, "rt", encoding="utf-8") as portrait_config_file:
    portrait_config = json.loads(portrait_config_file.read())

for character_name in list_characters:
    character_codename = ''.join(ch for ch in character_name if ch.isalnum())
    old_icon_path = f"./input/{character_name}/icon.png"
    old_portrait_path = f"./input/{character_name}/portrait.png"
    new_icon_path = f"{root_path}/base_files/icon/icon_smol_{character_codename}_00.png"
    new_portrait_path = f"{portrait_path}/costume_{character_codename}_00.png"

    character_data = {
        "codename": character_codename,
        "modded": True
    }

    eyesight_data = {
        "0": {
            "x": 0,
            "y": 0
      }
    }

    main_config["character_to_codename"][character_name] = character_data
    portrait_config["eyesights"][character_codename] = eyesight_data

    shutil.copy(old_icon_path, new_icon_path)
    # shutil.copy(old_portrait_path, new_portrait_path)

    portrait = Image.open(old_portrait_path).convert("RGBA")
    portrait = portrait.resize((int(portrait_scaling*portrait.size[0]), int(portrait_scaling*portrait.size[1])), Image.NEAREST)
    portrait.save(new_portrait_path)



with open(main_config_path, "wt", encoding="utf-8") as main_config_file:
    main_config_file.write(json.dumps(main_config, indent=2))

with open(portrait_config_path, "wt", encoding="utf-8") as portrait_config_file:
    portrait_config_file.write(json.dumps(portrait_config, indent=2, sort_keys=True))
