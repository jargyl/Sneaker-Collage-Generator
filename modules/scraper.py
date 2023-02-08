import time

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
    title = soup.find('title').string
    product_info = title.split(' - ')
    add_product_to_logs(product_info[1], url, size, FOUND_FILE, product_info[0])
    slug = url.replace(url[0:26], "")
    save_product_picture_with_size(slug, size, link)


def get_product_picture_from_sku(sku, size):
    sku = sku.upper()
    query_url = f"https://restocks.net/nl/shop/search?q={sku}&page=1"
    r = requests.get(query_url).json()
    if r['data']:
        product = r['data'][0]
        if product['sku'] == sku:
            product_picture = product['image']
            product_picture = product_picture.replace('400', '1000')
            print(product_picture)
            product_url = product['slug']
            product_name = product['name']

            r = requests.get(product_url)

            add_product_to_logs(sku, product_url, size, FOUND_FILE, product_name)
            slug = (product['slug']).replace((product['slug'])[0:26], "")
            save_product_picture_with_size(slug, size, product_picture)
        else:
            add_product_to_logs(sku, query_url, size, NOTFOUND_FILE)
    else:
        print("No match with SKU {}.".format(sku))


def add_product_to_logs(sku, url, size, path, product="NOT FOUND",):
    text = f"{product}\t{sku}\tEU {size}\t{url}"
    print("{:<50} {:<20}EU {:<15}".format(product, sku, size))
    file = open(path, 'a')
    file.write(text + "\n")
    file.close()


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
            while im.status_code != 200:
                print("error")
                time.sleep(10)
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
