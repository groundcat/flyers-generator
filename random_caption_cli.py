# -*- coding: utf-8 -*-

from PIL import Image, ImageFont, ImageDraw, ImageFilter, ImageEnhance
from string import ascii_letters
import textwrap
import os
import random
import csv
from dotenv import load_dotenv
import sys

# Usage: python3 random_caption_cli.py captions.csv original_EN fonts/Caveat/static/Caveat-Regular.ttf"

def main():
    """This ileterate each line in the text file
    and add a random image as its background."""

    # Load custom font
    font = ImageFont.truetype(font=FONT, size=90)
    logo_font = ImageFont.truetype(font=LOGO_FONT, size=72)

    # Load captions from csv file
    with open(CAPTIONS_CSV, "r", encoding="utf8") as captions_file:
        reader = csv.DictReader(captions_file)
        random_row = random.choice(list(reader))

        # Load the caption column from the row
        caption = random_row[CAPTIONS_COL_NAME]

        # Deal with special chars
        caption = caption.replace("’","'")
        print(f"Caption: {caption}")

        # Output file name
        output_name = ''.join(e for e in caption if e.isalnum())
        output_name = output_name[:10] + ".jpg"

        # Edit and save the image
        edit_image(caption, font, logo_font, output_name)


def edit_image(text, font, logo_font, output_name):

    while True:
        # Randomly select images

        image_file = random.choice(os.listdir(IMAGE_DIR))
        image_file_path = os.path.join(IMAGE_DIR, image_file)

        # Open image
        print(f"Processing image {image_file}")
        # img = Image.open(fp='images/spencer-bergen-kUU-TMPuiuo-unsplash.jpg', mode='r')
        try:
            img = Image.open(image_file_path, mode='r')
        except:
            continue

        # check if the orientation is landscape
        if img.size[0] > img.size[1]:
            break

    # Resize image
    new_height = round(img.size[1] * RESIZE_WIDTH / img.size[0])
    new_size = (RESIZE_WIDTH, new_height)
    img = img.resize(new_size)

    # Applying BoxBlur filter
    img = img.filter(ImageFilter.BoxBlur(5))

    # Change briteness of image
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(0.8)

    # Create DrawText object
    draw = ImageDraw.Draw(im=img)

    # Calculate the average length of a single character of our font.
    # Note: this takes into account the specific font and font size.
    avg_char_width = sum(font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)

    # Translate this average length into a character count
    max_char_count = int(img.size[0] * TEXT_WIDTH_PERCENT / avg_char_width)

    # Create a wrapped text object using scaled character count
    text = textwrap.fill(text=text, width=max_char_count)

    # Add text to the image
    draw.text(xy=(img.size[0]/2, img.size[1] / 2), text=text, font=font, fill='#FFFFFF', anchor='mm')
    draw.text(xy=(img.size[0]-200, img.size[1]-100), text=LOGO_TEXT, font=logo_font, fill='#FFFFFF', anchor='mm')

    # view the result
    # img.show()
    result_filename = "output/" + output_name
    print(f"Saving image to {result_filename}")
    img.save(result_filename)

    return output_name

if __name__ == "__main__" and len(sys.argv) == 4:

    # Load configuration from .env file
    load_dotenv()
    IMAGE_DIR = os.getenv('IMAGE_DIR')
    LOGO_TEXT = str(os.getenv('LOGO_TEXT'))
    LOGO_FONT = os.getenv('LOGO_FONT')
    TEXT_WIDTH_PERCENT = float(os.getenv('TEXT_WIDTH_PERCENT'))
    RESIZE_WIDTH = int(os.getenv('RESIZE_WIDTH'))

    # Load the command line arguments
    CAPTIONS_CSV = sys.argv[1]
    CAPTIONS_COL_NAME = sys.argv[2]
    FONT = sys.argv[3]

    # Print the arguments
    print("Captions CSV:", CAPTIONS_CSV)
    print("Captions column name:", CAPTIONS_COL_NAME)
    print("Font:", FONT)

    # Run the main function
    main()

else:
    print("Usage: python3 random_caption_cli.py captions.csv original_EN fonts/Caveat/static/Caveat-Regular.ttf")
