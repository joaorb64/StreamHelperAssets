from PIL import Image
import os
from pathlib import Path

source_dir_list = ["../../games/mhaaj/base_files/icon", "../../games/mhaaj/full"]
out_dir = "out"

Path(out_dir).mkdir(parents=True, exist_ok=True)

i = 1
for source_dir in source_dir_list:
    Path(f"{out_dir}/{i}").mkdir(parents=True, exist_ok=True)
    list_webp = []
    for file in os.listdir(source_dir):
        if file.endswith(".webp"):
            list_webp.append(file)

    for webp_file in list_webp:
        webp = Image.open(f"{source_dir}/{webp_file}").convert("RGBA")
        webp.save(f"{out_dir}/{i}/{webp_file}".replace(".webp", ".png"))

    i=i+1
