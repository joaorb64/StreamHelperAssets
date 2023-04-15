from PIL import Image
from glob import glob

file_list = glob("*.png")

for file_name in file_list:
    source = Image.open(file_name, "r").convert("RGBA")
    max_alpha = 0
    for x in range(source.width):
        for y in range(source.height):
            r, g, b, a = source.getpixel((x, y))
            if a > max_alpha:
                max_alpha = a
    factor = 255/max_alpha
    output = Image.new("RGBA", (source.width, source.height))
    for x in range(source.width):
        for y in range(source.height):
            r, g, b, a = source.getpixel((x, y))
            output.putpixel((x,y), (r,g,b,int(a*factor)))
    output.save(file_name)
