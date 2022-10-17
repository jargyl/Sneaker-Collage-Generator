import requests
from bs4 import BeautifulSoup
import csv
from PIL import Image, ImageDraw, ImageFont
import os.path


def get_items_from_csv():
    items = []
    with open('urls_size.csv') as csvfile:
        csvReader = csv.reader(csvfile)
        for row in csvReader:
            items.append(row)
    items.pop(0)
    return items


def get_product_picture(url, size):
    # GET PRODUCT IMAGE URL
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    images = soup.find_all('img')
    for image in images:
        link = image['src']
        if (link.startswith('https://media.restocks.net/products/')):
            break
    # GET PRODUCT NAME
    title_h1 = soup.find('div', {'class': 'product__title'}).find(
        "h1", recursive=False)
    # APPEND TO TEXT FILE
    product_names = open('names.txt', 'a')
    product_names.write(title_h1.text)
    product_names.write("\n");
    product_names.close()
    # SAVE IMAGE WITH TITLE
    title = (title_h1.text).replace(' ', '-')
    title += "_" + size
    path = "assets/{}".format(title);
    # Check if path exists
    if not (os.path.exists(path + ".png")):
        print(title);
        with open(path + '.png', 'wb') as f:
            im = requests.get(link)
            f.write(im.content)
        # ADD SIZE TO IMAGE
        im = Image.open("assets/" + title + '.png').convert('RGBA')
        title_font = ImageFont.truetype("arial.ttf", size=100)
        title_text = size
        image_editable = ImageDraw.Draw(im)
        image_editable.text((15,15), title_text, (0, 0, 0), font=title_font)
        im.save("assets/" + title + ".png")

# CLEAR TXT FILE
product_names = open('names.txt', 'w').close

items = get_items_from_csv()

for item in items:
    get_product_picture(item[0],item[1])
