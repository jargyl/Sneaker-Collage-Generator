from PIL import Image
import os

image_list = os.listdir("images")

COLLAGE_COUNT = 25
PATH = 'collage/'

height = 0
width = 0
count = 0
collage = Image.new("RGBA", size=(5000, 3000))

for index, i in enumerate(image_list):
    if (index != 0 and index % 25 == 0) or index == len(image_list):
        collage.save(PATH + 'collage{}.png'.format(count))
        collage = Image.new("RGBA", size=(5000, 3000))
        count += 1
        height = 0
        width = 0
    collage.paste(Image.open("images/{}".format(i)), (width, height))

    height += 600

    if height > 2400:
        width += 1000
        height = 0

collage.save(PATH + '/collage{}.png'.format(count))
