import cv2
import numpy as np
import pyscreenshot as ImageGrab
import time
import threading

class cv2CandySensor:
    def __init__(self):
        start_time = time.time()

        self.top_left = (133, 87)
        self.cell_size_h = 88
        self.cell_size_v = 78
        self.template_images_colors, self.template_images_variants = self.get_templates()

        print(f"Time to load templates: {time.time() - start_time}")

    def get_templates(self):
        candy_colors = ['blue', 'green', 'orange', 'purple', 'red', 'yellow']

        template_images_colors = {}
        template_images_variants = {}
        for color in candy_colors:
            template_images_colors[color] = cv2.imread(f'candies/{color}/{color}.png', cv2.IMREAD_UNCHANGED)

            template_images_variants[color+'_sh'] = cv2.imread(f'candies/{color}/{color}_sh.png', cv2.IMREAD_UNCHANGED)
            template_images_variants[color+'_sv'] = cv2.imread(f'candies/{color}/{color}_sv.png', cv2.IMREAD_UNCHANGED)
            template_images_variants[color+'_p'] = cv2.imread(f'candies/{color}/{color}_p.png', cv2.IMREAD_UNCHANGED)

        template_images_variants['Ñ'] = cv2.imread(f'candies/Special/special.png', cv2.IMREAD_UNCHANGED)
        return template_images_colors, template_images_variants

    def get_candy_matrix(self):
        start_time = time.time()

        bottom_right = (self.top_left[0] + 9 * self.cell_size_h, self.top_left[1] + 9 * self.cell_size_v)
        im = ImageGrab.grab(bbox=(self.top_left[0], self.top_left[1], bottom_right[0], bottom_right[1]))

        im_array = np.asarray(im)  # Convert the PIL image to a NumPy array

        candy_matrix = np.empty((9, 9), dtype=object)
        threads = []

        for i in range(9):
            for j in range(9):
                y1, y2 = i * self.cell_size_v, (i + 1) * self.cell_size_v
                x1, x2 = j * self.cell_size_h, (j + 1) * self.cell_size_h
                cell_im = im_array[y1:y2, x1:x2]  # Use array slicing on the NumPy array

                # Convert BGR to RGB
                cell_im_rgb = cv2.cvtColor(cell_im, cv2.COLOR_BGR2RGB)

                thread = threading.Thread(target=self.process_candy, args=(cell_im_rgb, candy_matrix, i, j))
                threads.append(thread)
                thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        print(f"Time to get candy matrix: {time.time() - start_time}")
        return candy_matrix

    def process_candy(self, image, candy_matrix, i, j):
        predicted_candy_color = self.classify_candy(image)
        candy_matrix[i, j] = predicted_candy_color[0] + ('_'+predicted_candy_color.split('_')[1] if '_' in predicted_candy_color else '')

    def classify_candy(self, image):
        best_match = None
        best_score = 0.0
        
        # First, check the main candy color
        for color, template in self.template_images_colors.items():
            result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            if max_val > 0.75:
                best_score = max_val
                best_match = color
                break

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
