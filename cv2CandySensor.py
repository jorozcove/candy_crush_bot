import cv2
import numpy as np
import pyscreenshot as ImageGrab

import time

class cv2CandySensor:
    def __init__(self):
        start_time = time.time()

        self.top_left = (133, 87)
        self.cell_size_h = 88
        self.cell_size_v = 78
        self.image_paths = 'actual_cells'
        self.template_images = self.get_templates()

        print(f"Time to load templates: {time.time() - start_time}")

    def get_templates(self, ):
        candy_colors = ['blue', 'green', 'orange', 'purple', 'red', 'yellow']

        template_images = {}
        for color in candy_colors:
            template_images[color] = cv2.imread(f'candies/{color}/{color}.png', cv2.IMREAD_UNCHANGED)
            template_images[color+'_sh'] = cv2.imread(f'candies/{color}/{color}_sh.png', cv2.IMREAD_UNCHANGED)
            template_images[color+'_sv'] = cv2.imread(f'candies/{color}/{color}_sv.png', cv2.IMREAD_UNCHANGED)
            template_images[color+'_p'] = cv2.imread(f'candies/{color}/{color}_p.png', cv2.IMREAD_UNCHANGED)

        template_images['Ñ'] = cv2.imread(f'candies/Special/special.png', cv2.IMREAD_UNCHANGED)
        return template_images

    def crop_cell(self, im, i,j):
        box = (i * self.cell_size_h, j * self.cell_size_v, (i + 1) * self.cell_size_h, (j + 1) * self.cell_size_v)
        cell_im = im.crop(box)
        return cell_im

    def get_candy_matrix(self):
        start_time = time.time()

        bottom_right = (self.top_left[0] + 9 * self.cell_size_h, self.top_left[1] + 9 * self.cell_size_v)
        im = ImageGrab.grab(bbox=(self.top_left[0], self.top_left[1], bottom_right[0], bottom_right[1]))

        candy_matrix = np.empty((9, 9), dtype=object)
        for i in range(9):
            for j in range(9):
                cell_im = self.crop_cell(im,j,i)

                img_path = f'{self.image_paths}/{i}_{j}.png'
                cell_im.save(img_path)

                predicted_candy_color = self.classify_candy(img_path, self.template_images)
                candy_matrix[i, j] = predicted_candy_color[0] + ('_'+predicted_candy_color.split('_')[1] if '_' in predicted_candy_color else '')

        print(f"Time to get candy matrix: {time.time() - start_time}")
        return candy_matrix

    def classify_candy(self, image_path, template_images):
        image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

        best_match = None
        best_score = 0.0
        
        for variant, template in template_images.items():
            result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            # if max_val > 0.75:
            #     best_match = variant
            #     break

            if max_val > best_score:
                best_score = max_val
                best_match = variant
        return best_match