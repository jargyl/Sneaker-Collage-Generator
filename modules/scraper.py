import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
import os.path

FOUND_FILE = "collage/product_found.txt"
NOTFOUND_FILE = "collage/product_not_found.txt"


def get_product_picture_from_url(url, size):
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
    product_title = soup.find('div', {'class': 'product__title'}).find(
        "h1", recursive=False)
    add_product_to_logs(product_title.text, size, FOUND_FILE)
    slug = url.replace(url[0:26], "")
    save_product_picture_with_size(slug, size, link)


def get_product_picture_from_sku(sku, size):
    sku = sku.upper()
    r = requests.get("https://restocks.net/nl/shop/search?q={}&page=1".format(sku)).json()
    if r['data']:
        product = r['data'][0]
        if product['sku'] == sku:
            product_picture = product['image']
            product_picture = product_picture.replace('400.png', '1000.png')
            product_name = product['name']
            add_product_to_logs(product_name, size, FOUND_FILE)
            slug = (product['slug']).replace((product['slug'])[0:26], "")
            save_product_picture_with_size(slug, size, product_picture)
        else:
            add_product_to_logs(sku, size, NOTFOUND_FILE)
    else:
        print("No match with SKU {}.".format(sku))


def add_product_to_logs(product, size, path):
    if path == FOUND_FILE:
        text = product + " - EU " + size
    else:
        text = f"{product} NOT FOUND"
    file = open(path, 'a')
    file.write(text + "\n")
    file.close()
    print(text)


def save_product_picture_with_size(name, size, img_url):
    clean_name = name.replace(' ', '-').replace('"', '')
    clean_size = size.replace(',', '.')
    if "/" in size:
        clean_size = size.replace('/', 'l').replace(' ', '_')
    else:
        clean_size = float(clean_size)

    filename = f"{clean_size}_{clean_name}"

    path = "collage/images/{}".format(filename)
    if not (os.path.exists(path + ".png")):
        with open(path + '.png', 'wb') as f:
            im = requests.get(img_url)
            f.write(im.content)
        # ADD SIZE TO IMAGE
        im = Image.open("collage/images/" + filename + '.png').convert('RGBA')
        title_font = ImageFont.truetype("arial.ttf", size=100)
        title_text = size.replace('_', ' ')
        image_editable = ImageDraw.Draw(im)
        image_editable.text((15, 15), title_text, (0, 0, 0), font=title_font)
        im.save("collage/images/" + filename + ".png")


def reset_logs():
    # CLEAR TXT FILE
    open(FOUND_FILE, 'w').close()
    open(NOTFOUND_FILE, 'w').close()
