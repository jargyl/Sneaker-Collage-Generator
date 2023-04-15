# Sneaker Image Collage Creator

A python project that allows users to upload a CSV file containing either the SKU or a URL of a sneaker along with its size. The program then downloads an image of the sneaker using web scraping (restocks.net) and adds its size to the image. The user can then create a collage of all the saved images with a customizable sizing.

## Installation

1. Clone the repository:
```
git clone https://github.com/username/sneaker-image-collage.git
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

## Usage

1. Upload a CSV file containing the SKU or a URL of a sneaker and its size. Here's an example of how the CSV file should look:

```
SKU, Size
DD1391-601, 46
https://restocks.net/nl/p/nike-dunk-low-retro-white-black-gs, 42.5
```

2. Run the program:

```
python main.py
```

You can now choose between 2 modules; 

  1. _SCRAPE_ for scraping the product images based on the csv-file. Product pictures with sizing will be saved in **'collage/images/'**. Products names that are found or not found will be saved in **'collage/product_found.txt'** & **'collage/product_not_found.txt'**

  2. _COLLAGE_ for making collages based on the pictures generated with the _SCRAPE_ module. Collages will be saved in **'collage/'**
  
## Example

![Collage](https://i.imgur.com/MnGJ9ws.png "Collage")


## License
This project is licensed under the MIT License. See the [MIT License](LICENSE) file for more information.
