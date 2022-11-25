from modules.scraper import reset_logs, get_product_picture_from_url, get_product_picture_from_sku
from modules.collage import create_collage
import time
import csv


def get_items_from_csv(path):
    item_list = []
    with open(path) as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            item_list.append(row)
    item_list.pop(0)
    # SORT BY SIZE
    item_list.sort(key=lambda x: x[1])
    return item_list


# PROMPT USER TO CHOOSE MODE
modes = ['SCRAPE', 'COLLAGE']
user_input = ''
input_message = "Choose a mode:\n"
for index, item in enumerate(modes):
    input_message += f'{index + 1}) {item}\n'
input_message += 'Your choice: '
while user_input not in map(str, range(1, len(modes) + 1)):
    user_input = input(input_message)
print('Starting ' + modes[int(user_input) - 1] + " mode ...")

start_time = time.time()
data = []
if user_input == "1":
    reset_logs()
    data = get_items_from_csv('scrape.csv')
    for p in data:
        if p[0].startswith("http"):
            get_product_picture_from_url(p[0], p[1])
        else:
            get_product_picture_from_sku(p[0], p[1])
if user_input == "2":
    print("Set dimensions of collage (eg. 3x4)")
    while True:
        try:
            horizontal = int(input("Width: "))
            vertical = int(input("Height: "))
            break
        except ValueError:
            print("Please enter a number")
    create_collage(vertical, horizontal)
print("Finished in %s seconds" % round((time.time() - start_time), 2))
