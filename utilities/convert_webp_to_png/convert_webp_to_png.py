from PIL import Image
import os

source_dir = "source"
out_dir = "out"

os.mkdir(out_dir)

list_webp = []
for file in os.listdir(source_dir):
    if file.endswith(".webp"):
        list_webp.append(file)

for webp_file in list_webp:
    webp = Image.open(f"{source_dir}/{webp_file}").convert("RGBA")
    webp.save(f"{out_dir}/{webp_file}".replace(".webp", ".png"))
