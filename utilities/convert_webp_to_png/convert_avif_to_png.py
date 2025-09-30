from PIL import Image
import os
from pathlib import Path

source_dir_list = ["../../games/riotpl/base_files/icon", "../../games/riotpl/website"]
out_dir = "out"

Path(out_dir).mkdir(parents=True, exist_ok=True)

i = 1
for source_dir in source_dir_list:
    Path(f"{out_dir}/{i}").mkdir(parents=True, exist_ok=True)
    list_avif = []
    for file in os.listdir(source_dir):
        if file.endswith(".avif"):
            list_avif.append(file)

    for avif_file in list_avif:
        avif = Image.open(f"{source_dir}/{avif_file}").convert("RGBA")
        avif.save(f"{out_dir}/{i}/{avif_file}".replace(".avif", ".png"))

    i=i+1