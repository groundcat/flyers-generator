from PIL import Image
import os

# assign directory
IMG_DIR = 'images'
RESIZE_WIDTH = 1920

# iterate over images in that directory
for filename in os.listdir(IMG_DIR):
    f = os.path.join(IMG_DIR, filename)
    # checking if it is a file
    if os.path.isfile(f):
        # Resize image
        img = Image.open(f, mode='r')
        new_height = round(img.size[1] * RESIZE_WIDTH / img.size[0])
        new_size = (RESIZE_WIDTH, new_height)
        img = img.resize(new_size)

    resized_filepath = "resized/" + filename
    img.save(resized_filepath)
    print(f"Saved resized image at {resized_filepath}")
