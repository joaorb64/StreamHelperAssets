import os
import shutil

files = [f for f in os.listdir() if f.endswith(".png")]

for f in files:
    filename = f.split(".png")[0]

    separated = filename.rsplit("_", 1)

    try:
        skin = separated[1]
        skin = int(skin)

        shutil.copy(f, f"new_folder/{separated[0]}_{skin-1:02d}.png")
    except:
        print("Error", f)
