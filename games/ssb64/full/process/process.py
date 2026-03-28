import os
import re
from PIL import Image

INPUT_DIR = "."
OUTPUT_DIR = "output"
NEGATIVE_IMAGE_PATH = "negative.png"

# Crop settings
CROP_X = 262
CROP_Y = 41
CROP_W = 1384
CROP_H = 988

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load negative image
negative_img = Image.open(NEGATIVE_IMAGE_PATH).convert("RGBA")
negative_pixels = list(negative_img.getdata())


# --- STEP 1: conservative pink detection ---
def create_mask(img):
    pixels = list(img.getdata())
    mask = []

    for (r, g, b, a) in pixels:
        is_bg = (
            r > 200 and
            b > 200 and
            g < 40 and
            abs(r - b) < 20
        )
        mask.append(1 if is_bg else 0)

    return mask


# --- STEP 2: dilate mask (expand 1 pixel) ---
def dilate_mask(mask, width, height):
    new_mask = mask.copy()

    for y in range(height):
        for x in range(width):
            i = y * width + x

            if mask[i] == 1:
                continue

            neighbors = [
                (x-1, y), (x+1, y),
                (x, y-1), (x, y+1),
            ]

            for nx, ny in neighbors:
                if 0 <= nx < width and 0 <= ny < height:
                    ni = ny * width + nx
                    if mask[ni] == 1:
                        new_mask[i] = 1
                        break

    return new_mask


# --- STEP 3: apply mask + negative ---
def process_image(img):
    img = img.convert("RGBA")
    width, height = img.size
    pixels = list(img.getdata())

    # Build mask
    mask = create_mask(img)

    # Expand it to kill pink fringes
    mask = dilate_mask(mask, width, height)
    # Uncomment if needed:
    # mask = dilate_mask(mask, width, height)

    new_pixels = []

    for i, (r, g, b, a) in enumerate(pixels):
        _, _, _, na = negative_pixels[i]

        if mask[i] == 1 or na > 0:
            new_pixels.append((r, g, b, 0))  # fully transparent
        else:
            new_pixels.append((r, g, b, 255))  # fully opaque

    img.putdata(new_pixels)
    return img


def process_file(filename):
    match = re.match(r"(.+?)_(\d+)\.png$", filename)
    if not match:
        return

    name, num = match.groups()
    new_index = int(num) - 1
    new_filename = f"{name}_{new_index}.png"

    input_path = os.path.join(INPUT_DIR, filename)
    output_path = os.path.join(OUTPUT_DIR, new_filename)

    img = Image.open(input_path)

    # Crop first
    img = img.crop((
        CROP_X,
        CROP_Y,
        CROP_X + CROP_W,
        CROP_Y + CROP_H
    ))

    # Ensure size matches negative mask
    if img.size != negative_img.size:
        raise ValueError(f"Size mismatch: {filename} vs negative image")

    img = process_image(img)

    img.save(output_path)
    print(f"Processed: {filename} -> {new_filename}")


def main():
    for file in os.listdir(INPUT_DIR):
        if file.lower().endswith(".png") and file != NEGATIVE_IMAGE_PATH:
            process_file(file)


if __name__ == "__main__":
    main()
