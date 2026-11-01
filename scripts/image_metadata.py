"""
Writes "image_sizes" and "average_size" into the config.json of asset packs.

With --changes, only the packs changed since the last processed commit are
scanned; without it, every pack under games/ is.
"""
import argparse
import json
import os
import re
from PIL import Image

from asset_changes import load_changes

Image.MAX_IMAGE_PIXELS = None

BASE_DIR = "games"
IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')


def is_game_base_config(root):
    """games/<game>/base_files/config.json holds game data, not image data."""
    parts = os.path.normpath(root).split(os.sep)
    return len(parts) == 3 and parts[2] == "base_files"


def process_config(root, files):
    config_path = os.path.join(root, 'config.json')

    with open(config_path, "rt", encoding="utf-8") as config_file:
        original = config_file.read()
    config = json.loads(original)

    scaling = config.get("rescaling_factor", {})
    regex = re.compile(config.get("prefix", "") + "(.*)" +
                       config.get("postfix", "") + "(.*)\\.([A-Za-z0-9]*)")

    sizes_dict = {}
    total_width = 0.0
    total_height = 0.0
    image_count = 0

    for file in sorted(files):
        if not file.lower().endswith(IMAGE_EXTENSIONS):
            continue
        image_path = os.path.join(root, file)
        regex_search = regex.search(file)
        if not regex_search:
            print(f"Error processing image {image_path}: Image name did not match config")
            continue
        try:
            codename, index = regex_search.group(1), regex_search.group(2)
            if index:
                index = str(int(index))
                scaling_factor = scaling.get(codename, {}).get(
                    index, scaling.get(codename, {}).get("0", 1.0))
            else:
                index = "null"
                scaling_factor = 1.0
            with Image.open(image_path) as img:
                width, height = img.size
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
            continue

        sizes_dict.setdefault(codename, {})[index] = {"x": width, "y": height}
        total_width += width * scaling_factor
        total_height += height * scaling_factor
        image_count += 1

    if image_count == 0:
        print(f"No images found in {root}")
        return

    config['image_sizes'] = {
        codename: dict(sorted(indexes.items()))
        for codename, indexes in sorted(sizes_dict.items())
    }
    config['average_size'] = {
        "x": total_width / image_count,
        "y": total_height / image_count
    }

    updated = json.dumps(config, indent=2)
    if updated != original:
        with open(config_path, "wt", encoding="utf-8") as config_file:
            config_file.write(updated)
        print(f"Updated {config_path}")


def process_pack(pack_dir):
    for root, dirs, files in os.walk(pack_dir):
        dirs.sort()
        if 'config.json' in files and not is_game_base_config(root):
            process_config(root, files)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--changes")
    args = parser.parse_args()

    if args.changes:
        packs = load_changes(args.changes)["packs"]
    else:
        packs = [
            os.path.join(BASE_DIR, game, pack)
            for game in sorted(os.listdir(BASE_DIR))
            if os.path.isdir(os.path.join(BASE_DIR, game))
            for pack in sorted(os.listdir(os.path.join(BASE_DIR, game)))
        ]

    for pack in packs:
        if os.path.isdir(pack):
            process_pack(pack)


if __name__ == "__main__":
    main()
