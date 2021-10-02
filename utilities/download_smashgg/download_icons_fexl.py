import json
import requests
from pathlib import Path

with open(f"download/config.json", 'rt') as config_file:
    config = json.loads(config_file.read())
    characters_data:dict = config.get("character_to_codename")

full_dir = "full"
Path(full_dir).mkdir(parents=True, exist_ok=True)

for character in characters_data.keys():
    icon_filename = f'{characters_data.get(character).get("codename")}'
    with open(f"download/icon/{icon_filename}_0.png", 'wb') as f:
        image_file = requests.get(f"https://www.arika.co.jp/special/sp_material/ma_fexl/{icon_filename}.png")
        f.write(image_file.content)
    
    with open(f"full/{icon_filename}_0.png", 'wb') as f:
        image_file = requests.get(f"https://www.arika.co.jp/special/sp_material/ma_fexl/{icon_filename}_all.png")
        f.write(image_file.content)
