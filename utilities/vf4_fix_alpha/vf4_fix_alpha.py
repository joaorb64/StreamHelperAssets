from PIL import Image
import statistics

source = "123496.png"
dest = "out.png"

img = Image.open(source, 'r')
red, green, blue, alpha = img.split()

list_alpha_values = []
for x in range(img.width):
        for y in range(img.height):
            alpha_value = alpha.getpixel((x, y))
            if alpha_value != 0:
                list_alpha_values.append(alpha_value)

median_alpha = statistics.median(list_alpha_values)

for x in range(img.width):
        for y in range(img.height):
            alpha_value = alpha.getpixel((x, y))
            new_alpha_value = float(alpha_value)/median_alpha * 255.0
            if new_alpha_value > 255.0:
                new_alpha_value = 255.0
            new_alpha_value = round(new_alpha_value)
            alpha.putpixel((x, y), new_alpha_value)

img.putalpha(alpha)
img.save(dest)