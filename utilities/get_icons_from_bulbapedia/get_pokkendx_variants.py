from PIL import Image
import json
import requests
import caseutil
import io

game_path = "../../games/pokkendx"
config_path = f"{game_path}/base_files/config.json"
variant_path = f"{game_path}/variant_icon"
prefix, suffix = "file_", ""
source_base_url = "https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen7x/regular"

with open(config_path, 'rt', encoding="utf-8") as config_file:
    config_dict = json.loads(config_file.read())
    variant_dict = config_dict.get("variant_to_codename")

for variant in variant_dict.keys():
    print(variant)
    pokemon_list = variant.split(" / ")
    variant_image = Image.new('RGBA', size=(96,48), color=(0,0,0,0))
    variant_codename = variant_dict[variant].get("codename")

    for i in range(len(pokemon_list)):
        pokemon = pokemon_list[i]
        pokemon_kebab = caseutil.to_kebab(pokemon)
        if 'rayquaza' in pokemon_kebab:
            pokemon_kebab = "rayquaza-mega"
        if 'farfetch' in pokemon_kebab:
            pokemon_kebab = "farfetchd"
        pokemon_url = f"{source_base_url}/{pokemon_kebab}.png"
        response = requests.get(pokemon_url)
        assert response.status_code == 200
        pokemon_image = Image.open(io.BytesIO(response.content))
        pokemon_image = pokemon_image.convert("RGBA")
        
        if i == 0:
            position = (-10, -8)
        else:
            position = (38, -8)
        
        variant_image.paste(pokemon_image, position, pokemon_image)

    image_path = f"{variant_path}/{prefix}{variant_codename}{suffix}.png"
    variant_image.save(image_path)
