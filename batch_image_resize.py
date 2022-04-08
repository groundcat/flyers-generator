from PIL import Image
import os
import sys

# Usage: python3 batch_image_resize.py path_to_images_directory"

# Validate the CLI arguments
if len(sys.argv) != 3:
    print("Usage: python3 batch_image_resize.py path_to_images_directory path_to_output_directory")
    exit(1)

# assign directory
IMG_DIR = sys.argv[1]
OUTPUT_DIR = sys.argv[2]
RESIZE_WIDTH = 1920
LANDSCAPE_ONLY = True # Set this to True if you only want to resize landscape images

# iterate over images in that directory
for filename in os.listdir(IMG_DIR):
    print(f"Checking the file {filename}")
    f = os.path.join(IMG_DIR, filename)
    # checking if it is a file
    if os.path.isfile(f):
        # Resize image
        img = Image.open(f, mode='r')
        new_height = round(img.size[1] * RESIZE_WIDTH / img.size[0])
        new_size = (RESIZE_WIDTH, new_height)

        # check if the orientation is landscape
        if LANDSCAPE_ONLY:
            if img.size[0] < img.size[1]:
                print("Skipping non-landscape image")
                continue
        
        # Resize image
        img = img.resize(new_size)
    else:
        print("Not a file")
        break

    resized_filepath = OUTPUT_DIR + "/" + filename
    img.save(resized_filepath)
    print(f"Saved resized image at {resized_filepath}")
