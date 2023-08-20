#Resize all images in all folders yo a h, v size
import os
from PIL import Image


def resize_images(path, h, v):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".png") or file.endswith(".bmp"):
                image = Image.open(os.path.join(root, file))
                image = image.resize((h, v), Image.ANTIALIAS)
                image.save(os.path.join(root, file))

new_folder = 'candies_pc2'
resize_images(new_folder, 71, 63)