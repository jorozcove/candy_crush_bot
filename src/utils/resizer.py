#Resize all images in all folders yo a h, v size
import os
from PIL import Image

def resize_images(w, h, path):

    new_path = os.path.join(os.getcwd(), f'{path}{w}x{h}')
    
    os.makedirs(new_path)
    print(f"New path: {new_path}")

    root = os.path.join(os.getcwd(), path)
    dirs = os.listdir(root)

    for dir in dirs:
        os.makedirs(os.path.join(new_path, dir))

        for file in os.listdir(os.path.join(root, dir)):
            if file.endswith(".png") or file.endswith(".bmp"):
                image = Image.open(os.path.join(root, dir, file))
                image = image.resize((w, h), Image.ANTIALIAS)

                image.save(os.path.join(new_path, dir, file))

    return new_path 