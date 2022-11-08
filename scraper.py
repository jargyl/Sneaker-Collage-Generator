import requests
from bs4 import BeautifulSoup
import csv
from PIL import Image, ImageDraw, ImageFont
import os.path


def get_items_from_csv(path):
    items = []
    with open(path) as csvfile:
        csvReader = csv.reader(csvfile)
        for row in csvReader:
            items.append(row)
    items.pop(0)
    return items


def get_product_picture_from_url(url, logfile, size):
    # GET PRODUCT IMAGE URL
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    images = soup.find_all('img')
    link = ""
    for image in images:
        link = image['src']
        if link.startswith('https://media.restocks.net/products/'):
            break
    # GET PRODUCT NAME
    title_h1 = soup.find('div', {'class': 'product__title'}).find(
        "h1", recursive=False)
    add_product_name_to_logs(title_h1.text, logfile)
    save_product_picture_with_size(title_h1.text, size, link)


def get_product_picture_from_sku(sku, logfile, size):
    sku = sku.upper()
    r = requests.get("https://restocks.net/nl/shop/search?q={}&page=1".format(sku)).json()
    if r['data']:
        data = r['data'][0]
        if data['sku'] == sku:
            product_picture = data['image']
            product_picture = product_picture.replace('400.png', '1000.png')
            product_name = data['name']
            print(product_name, product_picture)
            add_product_name_to_logs(product_name, logfile)
            save_product_picture_with_size(product_name, size, product_picture)
        else:
            print('No exact match with SKU {} found.'.format(sku))
    else:
        print("No match with SKU {}.".format(sku))


def add_product_name_to_logs(name, path):
    file = open(path, 'a')
    file.write(name)
    file.write("\n")
    file.close()


def save_product_picture_with_size(name, size, img_url):
    name = name.replace(' ', '-').replace('"', '')
    size = size.replace('/', 'l')
    name += "_" + size
    path = "assets/{}".format(name)
    if not (os.path.exists(path + ".png")):
        with open(path + '.png', 'wb') as f:
            im = requests.get(img_url)
            f.write(im.content)
        # ADD SIZE TO IMAGE
        im = Image.open("assets/" + name + '.png').convert('RGBA')
        title_font = ImageFont.truetype("arial.ttf", size=100)
        title_text = size
        image_editable = ImageDraw.Draw(im)
        image_editable.text((15, 15), title_text, (0, 0, 0), font=title_font)
        im.save("assets/" + name + ".png")


# CLEAR TXT FILE
product_names = open('names.txt', 'w').close

items = get_items_from_csv('scrape_sku.csv')

for item in items:
    get_product_picture_from_sku(item[0], 'names.txt', item[1])
