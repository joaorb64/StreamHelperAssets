from glob import glob
import shutil
from pathlib import Path

root_path = "../../games/pkmn"
full_path = f"{root_path}/full"

Path("forms").mkdir(exist_ok=True)

all_files = glob(f"{full_path}/*.png")

for file_path in all_files:
    if not file_path.removesuffix(".png").endswith("_0"):
        shutil.copy(file_path, "forms/")