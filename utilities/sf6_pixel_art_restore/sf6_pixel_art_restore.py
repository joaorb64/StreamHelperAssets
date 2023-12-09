from PIL import Image
from glob import glob
from statistics import mode
from pathlib import Path
from os.path import basename as get_file_name
import json

result_folder_name = "sf6/pixel_art_restore"
Path(result_folder_name).mkdir(parents=True, exist_ok=True)

target_size=128

og_files = glob("../../games/sf6/pixel_art/*.png")
og_config_path = "../../games/sf6/pixel_art/config.json"
upscale_factor = int(3840/target_size)+1

for og_path in og_files:
    og_image = Image.open(og_path).convert("RGBA")
    og_width, og_height = og_image.width, og_image.height
    sampling_ratio = og_height/target_size
    print(sampling_ratio)
    new_width, new_height = int(
        og_width/sampling_ratio), int(og_height/sampling_ratio)
    new_image = Image.new("RGBA", (new_width, new_height))
    for new_pixel_x in range(new_width):
        for new_pixel_y in range(new_height):
            # calculating_pixel_color
            list_r, list_g, list_b, list_a = list(), list(), list(), list()
            for offset_x in range(int(sampling_ratio)):
                for offset_y in range(int(sampling_ratio)):
                    pixel_color = og_image.getpixel(
                        (new_pixel_x*sampling_ratio + offset_x, new_pixel_y*sampling_ratio + offset_y))
                    list_r.append(pixel_color[0])
                    list_g.append(pixel_color[1])
                    list_b.append(pixel_color[2])
                    list_a.append(pixel_color[3])
            r, g, b, a = int(mode(list_r)), int(mode(
                list_g)), int(mode(list_b)), int(mode(list_a))
            if a == 0:
                r, g, b, a = 0, 0, 0, 0
            # elif a < 255:
            #     alpha_ratio = 255/a
            #     r, g, b, a = int(
            #         alpha_ratio*r), int(alpha_ratio*g), int(alpha_ratio*b), 255
            new_image.putpixel((new_pixel_x, new_pixel_y), (r, g, b, a))
    new_path = f"{result_folder_name}/{get_file_name(og_path)}"
    new_image = new_image.resize((int(new_width*upscale_factor), int(new_height*upscale_factor)), Image.Resampling.NEAREST)
    new_image.save(new_path)

new_config_path = f"{result_folder_name}/config.json"
with open(og_config_path, "rt", encoding="utf-8") as og_config_file:
    with open(new_config_path, "wt", encoding="utf-8") as new_config_file:
        config = json.loads(og_config_file.read())
        config["name"] = f'{config["name"]} (Cleaned up)'
        config["description"] = f'{config["description"]}\nCleaned up programmatically to remove extraction artefacts and integer upscaled to 4K'
        for codename in config.get("eyesights").keys():
            for skin in config.get("eyesights").get(codename).keys():
                for coordinate in config.get("eyesights").get(codename).get(skin).keys():
                    config["eyesights"][codename][skin][coordinate] = int((config["eyesights"][codename][skin][coordinate]/sampling_ratio)*upscale_factor)
        new_config_file.write(json.dumps(config, indent=2))
