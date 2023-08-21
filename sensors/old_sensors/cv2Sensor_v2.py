import cv2
import numpy as np
import pyscreenshot as ImageGrab
import time

class cv2CandySensor:
    def __init__(self, x, y, cell_size_w, cell_size_h, templates_path):
        start_time = time.time()

        self.top_left = (x, y)
        self.cell_size_w = cell_size_w
        self.cell_size_h = cell_size_h
        self.templates_path = templates_path
        self.template_images_colors, self.template_images_variants = self.get_templates()

        print(f"Time to load templates: {time.time() - start_time}")

    def get_templates(self):
        candy_colors = ['blue', 'green', 'orange', 'purple', 'red', 'yellow']

        template_images_colors = {}
        template_images_variants = {}
        for color in candy_colors:
            template_images_colors[color] = cv2.imread(f'{self.templates_path}/{color}/{color}.png', cv2.IMREAD_UNCHANGED)

            template_images_variants[color+'_sh'] = cv2.imread(f'{self.templates_path}/{color}/{color}_sh.png', cv2.IMREAD_UNCHANGED)
            template_images_variants[color+'_sv'] = cv2.imread(f'{self.templates_path}/{color}/{color}_sv.png', cv2.IMREAD_UNCHANGED)
            template_images_variants[color+'_p'] = cv2.imread(f'{self.templates_path}/{color}/{color}_p.png', cv2.IMREAD_UNCHANGED)

        template_images_variants['Ñ'] = cv2.imread(f'{self.templates_path}/Special/special.png', cv2.IMREAD_UNCHANGED)
        return template_images_colors, template_images_variants

    def get_candy_matrix(self):
        start_time = time.time()

        bottom_right = (self.top_left[0] + 9 * self.cell_size_w, self.top_left[1] + 9 * self.cell_size_h)
        im = ImageGrab.grab(bbox=(self.top_left[0], self.top_left[1], bottom_right[0], bottom_right[1]))

        im_array = np.asarray(im)  # Convert the PIL image to a NumPy array

        candy_matrix = np.empty((9, 9), dtype=object)
        for i in range(9):
            for j in range(9):
                y1, y2 = i * self.cell_size_h, (i + 1) * self.cell_size_h
                x1, x2 = j * self.cell_size_w, (j + 1) * self.cell_size_w
                cell_im = im_array[y1:y2, x1:x2]  # Use array slicing on the NumPy array

                # Convert BGR to RGB
                cell_im_rgb = cv2.cvtColor(cell_im, cv2.COLOR_BGR2RGB)

                predicted_candy_color = self.classify_candy(cell_im_rgb)
                candy_matrix[i, j] = predicted_candy_color[0] + ('_'+predicted_candy_color.split('_')[1] if '_' in predicted_candy_color else '')

        print(f"Time to get candy matrix: {time.time() - start_time}")
        return candy_matrix

    def classify_candy(self, image):
        best_match = None
        best_score = 0.0
        
        # First, check the main candy color
        for color, template in self.template_images_colors.items():
            result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            # if max_val > 0.75:
            #     best_score = max_val
            #     best_match = color
            #     break

            if max_val > best_score:
                best_score = max_val
                best_match = color
        
        # Then, check the variants of the best_match color
        for variant, template in self.template_images_variants.items():
            if variant.startswith(best_match):
                result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                if max_val > best_score:
                    best_score = max_val
                    best_match = variant
        
        return best_match
