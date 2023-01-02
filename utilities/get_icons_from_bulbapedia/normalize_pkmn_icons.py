from PIL import Image
import glob

icon_folder = "../../games/pkmn/base_files/icon/"
file_list = glob.glob(f"{icon_folder}/*.png")
target_size = 256

for filename in file_list:
    im = Image.open(filename)
    width, height = im.size
    factor = min(int(float(target_size)/float(width)), int(float(target_size)/float(height))) + 1
    width, height = round(width*factor), round(height*factor)
    # print(width, height, factor)
    if factor > 2:
        im = im.resize((width, height), Image.NEAREST)
        im.save(filename)