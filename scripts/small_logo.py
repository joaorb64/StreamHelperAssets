import os
from PIL import Image

def resize_logo(base_dir):
	for root, _, files in os.walk(base_dir):
		for file in files:
			if file == 'logo.png':
				logo_path = os.path.join(root, file)
				small_logo_path = os.path.join(root, 'logo_small.png')
				if not os.path.exists(small_logo_path):
					img = Image.open(logo_path)
					width_percent = (128 / float(img.size[0]))
					height_size = int((float(img.size[1]) * float(width_percent)))
					img = img.resize((128, height_size), Image.LANCZOS)
					img.save(small_logo_path)
					print(f'Resized and saved: {small_logo_path}')

if __name__ == "__main__":
	base_dir = 'games'
	resize_logo(base_dir)