# -*- coding: utf-8 -*-

from PIL import Image, ImageFont, ImageDraw, ImageFilter, ImageEnhance
from string import ascii_letters
import textwrap
import os
import random
import csv
import base64
import requests
import json
from dotenv import load_dotenv
import shutil
import sys
import re


# Usage: python3 ifttt_webhook_cli.py captions.csv original_EN fonts/Caveat/static/Caveat-Regular.ttf"

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

        # Trim to remove whitespace
        caption = caption.strip()

        # Output file name
        output_name = ''.join(e for e in caption if e.isalnum())
        output_name = output_name[:10] + ".jpg"

        # Edit and save the image
        edit_image(caption, font, logo_font, output_name)

        # Upload the image to imgbb
        img_path = "output/" + output_name 
        img_url = imgbb(img_path)

        # Trigger IFTTT webhook
        ifttt(caption, img_url)

        # Delete the contents in the directory
        delete_folder("output/")


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

    # Determine if the font contains Chinese characters
    if re.search(u'[\u4e00-\u9fff]+', text):
        # Chinese characters
        max_char_count = 13

    else:
        # English characters
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

def imgbb(img_path):
    
    print("API Key: " + IMGBB_KEY)

    with open(img_path, "rb") as file:
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": IMGBB_KEY,
            "image": base64.b64encode(file.read()),
        }
        response = requests.post(url, payload)

    if response.status_code == 200:
        print("Server Response: " + str(response.status_code))
        print("Successfully uploaded to imgbb")

        # Parse JSON response from API
        data = response.text
        parsed = json.loads(data)

        # Print the parsed JSON response
        print(json.dumps(parsed, indent=4))

        # Get the uploaded image URL
        url = parsed["data"]["url"]

        # Print the URL
        print(f"The URL is {url}")

        # Return the URL
        return url

    else:
        print("ERROR uploading to imgbb, Server Response: " + str(response.status_code))
        exit(1)
    
def ifttt(var1, var2):

    # Make POST request
    url = "https://maker.ifttt.com/trigger/" + IFTTT_EVENT + "/with/key/" + IFTTT_KEY
    payload = {
        "value1": var1,
        "value2": var2,
    }
    response = requests.post(url, payload)

    if response.status_code == 200:
        print("Server Response: " + str(response.status_code))
        print("Successfully triggered IFTTT webhook")

    else:
        print("ERROR with IFTTT webhook Server Response: " + str(response.status_code))
        exit(1)

def delete_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
            print("Deleted the folder successfully")
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))

# Validate the arguments and call the main function
if __name__ == "__main__" and len(sys.argv) == 4:

    # Load configuration from .env file
    load_dotenv()
    IMAGE_DIR = os.getenv('IMAGE_DIR')
    LOGO_TEXT = str(os.getenv('LOGO_TEXT'))
    LOGO_FONT = os.getenv('LOGO_FONT')
    TEXT_WIDTH_PERCENT = float(os.getenv('TEXT_WIDTH_PERCENT'))
    RESIZE_WIDTH = int(os.getenv('RESIZE_WIDTH'))

    # ImgBB config
    IMGBB_KEY = os.getenv('IMGBB_KEY')

    # IFTTT config
    IFTTT_EVENT = os.getenv('IFTTT_EVENT')
    IFTTT_KEY = os.getenv('IFTTT_KEY')

    # Load the command line arguments
    CAPTIONS_CSV = sys.argv[1]
    CAPTIONS_COL_NAME = sys.argv[2]
    FONT = sys.argv[3]

    # Print the arguments
    print("Captions CSV:", CAPTIONS_CSV)
    print("Captions column name:", CAPTIONS_COL_NAME)
    print("Font:", FONT)

    # Call the main function
    main()

else:
    print("Usage: python3 ifttt_webhook_cli.py captions.csv original_EN fonts/Caveat/static/Caveat-Regular.ttf")
