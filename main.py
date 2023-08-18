import numpy as np
import pyscreenshot as ImageGrab
import os
from sensor import classify_candy, get_templates

def crop_cell(im, i,j):
    # Crop the image to get the cell
    box = (i * cell_size_h, j * cell_size_v, (i + 1) * cell_size_h, (j + 1) * cell_size_v)
    cell_im = im.crop(box)
    return cell_im

top_left = (133, 87)
cell_size_h = 88
cell_size_v = 78
image_paths = 'actual_cells'

def main(template_images):
    bottom_right = (top_left[0] + 9 * cell_size_h, top_left[1] + 9 * cell_size_v)
    im = ImageGrab.grab(bbox=(top_left[0], top_left[1], bottom_right[0], bottom_right[1]))

    candy_matrix = np.empty((9, 9), dtype=object)
    for i in range(9):
        for j in range(9):
            cell_im = crop_cell(im,j,i)

            img_path = f'{image_paths}/{i}_{j}.png'
            cell_im.save(img_path)

            predicted_candy_color = classify_candy(img_path, template_images)
            candy_matrix[i, j] = predicted_candy_color[0] + ('_'+predicted_candy_color.split('_')[1] if '_' in predicted_candy_color else '')

    print(candy_matrix)


if __name__ == '__main__':
    template_images = get_templates()
    while True:
        main(template_images)
        input("Enter to continue...")


