"""
Creates logo_small.png next to every logo.png that has none, and regenerates
it when logo.png changed (unless logo_small.png was changed by hand too).

With --changes, only the packs changed since the last processed commit are
scanned; without it, all of games/ is.
"""
import argparse
import os
from PIL import Image

from asset_changes import load_changes


def resize_logo(base_dir, changed_paths=frozenset()):
	for root, _, files in os.walk(base_dir):
		if 'logo.png' not in files:
			continue
		logo_path = os.path.join(root, 'logo.png')
		small_logo_path = os.path.join(root, 'logo_small.png')
		logo_changed = logo_path.replace(os.sep, "/") in changed_paths
		small_changed = small_logo_path.replace(os.sep, "/") in changed_paths
		if os.path.exists(small_logo_path) and (not logo_changed or small_changed):
			continue
		with Image.open(logo_path) as img:
			width_percent = (128 / float(img.size[0]))
			height_size = int((float(img.size[1]) * float(width_percent)))
			img = img.resize((128, height_size), Image.LANCZOS)
			img.save(small_logo_path)
		print(f'Resized and saved: {small_logo_path}')


def main():
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--changes")
	args = parser.parse_args()

	if not args.changes:
		resize_logo('games')
		return

	changes = load_changes(args.changes)
	changed_paths = frozenset(f["path"] for f in changes["files"])
	for pack in changes["packs"]:
		if os.path.isdir(pack):
			resize_logo(pack, changed_paths)


if __name__ == "__main__":
	main()
