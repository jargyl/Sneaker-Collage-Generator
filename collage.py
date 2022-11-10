from PIL import Image
import os

IMAGE_LIST = os.listdir("images")
IMAGE_WIDTH = 1000
IMAGE_HEIGHT = 600
PATH = 'collage/'


def create_collage(vertical, horizontal):
    empty_folder()
    # TOTAL PICTURES IN SINGLE CANVAS
    total = vertical * horizontal

    # DIMENSIONS OF CANVAS
    width = horizontal * IMAGE_WIDTH
    height = vertical * IMAGE_HEIGHT
    collage = Image.new("RGBA", size=(width, height))

    x_range = 0
    y_range = 0
    count = 1
    for index, i in enumerate(IMAGE_LIST):
        # CREATE NEW CANVAS IF CANVAS REACHES MAX CAPACITY
        if index != 0 and index % total == 0:
            collage.save(PATH + 'collage{}.png'.format(count))
            collage = Image.new("RGBA", size=(width, height))
            count += 1
            x_range = 0
            y_range = 0

        collage.paste(Image.open("images/{}".format(i)), (x_range, y_range))

        # MOVE PASTE COORDINATES BY THE SIZE OF ONE IMAGE
        x_range += IMAGE_WIDTH
        if x_range == width:
            y_range += IMAGE_HEIGHT
            x_range = 0
    collage.save(PATH + '/collage{}.png'.format(count))


def empty_folder():
    for f in os.listdir(PATH):
        os.remove(os.path.join(PATH, f))
