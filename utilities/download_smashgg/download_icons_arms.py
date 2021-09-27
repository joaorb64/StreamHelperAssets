import json
import requests
from pathlib import Path

download_folder_name = "download"
Path(download_folder_name).mkdir(parents=True, exist_ok=True)

with open(f"{download_folder_name}/config.json", 'wt') as config_file:
    with open(f"{download_folder_name}/README.md", 'wt') as readme_file:
        Path(f"{download_folder_name}/icon").mkdir(parents=True, exist_ok=True)
        with open(f"{download_folder_name}/icon/config.json", 'wt') as icon_config_file:

            characters_file = requests.get("https://api.smash.gg/characters")

            game_name = "ARMS"
            game_id = 193
            description = "Base config to use this game."
            credits = ''

            characters_file_content = characters_file.json()

            characters = characters_file_content.get("entities").get("character")

            config_dict: dict = {
                "name": str(game_name),
                "smashgg_game_id": game_id,
                "character_to_codename": {},
                "stage_to_codename": {},
                "version": "0.1",
                "description": str(description),
                "credits": str(credits)
            }

            readme_file_content = f"""
            # {game_name}

            ## Description:
            {description}

            ## Credits:
            {credits}
            """.replace("            ", "")
            icon_config_dict = {
                "prefix": "icon_",
                "postfix": "_",
                "type": ["icon"]
            }

            for character in characters:
                if character.get("videogameId") == game_id:
                    name:str = character.get("name")
                    print(name)
                    codename = name.replace(' ', '').replace('&', '').replace('.', '')
                    value = {
                        "smashgg_name": name,
                        "codename": codename
                    }
                    config_dict["character_to_codename"][name] = value
                    for image_data in character.get("images"):
                        if image_data.get("type") == "stockIcon" and image_data.get("width")==32:
                            image_file = requests.get(image_data.get("url"))
                            image_filename = f"icon_{codename}_0.png"
                            with open(f"{download_folder_name}/icon/{image_filename}", 'wb') as f:
                                f.write(image_file.content)

            config_file_content = json.dumps(config_dict, indent=2)
            config_file.write(config_file_content)
            readme_file.write(readme_file_content)
            icon_config_file_content = json.dumps(icon_config_dict, indent=2)
            icon_config_file.write(icon_config_file_content)
