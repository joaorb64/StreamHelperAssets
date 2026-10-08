from PIL import Image
import os
from pathlib import Path

source_dir_list = ["../../games/ssbwiiu/stage_icon"]
out_dir = "out"

Path(out_dir).mkdir(parents=True, exist_ok=True)

i = 1
for source_dir in source_dir_list:
    Path(f"{out_dir}/{i}").mkdir(parents=True, exist_ok=True)
    list_jpg = []
    for file in os.listdir(source_dir):
        if file.endswith(".jpg") or file.endswith(".JPG"):
            list_jpg.append(file)

    for jpg_file in list_jpg:
        jpg = Image.open(f"{source_dir}/{jpg_file}").convert("RGBA")
        jpg.save(f"{out_dir}/{i}/{jpg_file}".replace(".JPG", ".png").replace(".jpg", ".png"))

    i=i+1
