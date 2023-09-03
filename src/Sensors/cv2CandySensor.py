import cv2
import numpy as np
import pyscreenshot as ImageGrab
import time
import threading
import pyautogui

from .windowcapture import WindowCapture

class cv2CandySensor:
    def __init__(self, x, y, cell_size_w, cell_size_h, templates_path):
        start_time = time.time()

        print(f"x = {x}, y = {y}, cell_size_w = {cell_size_w}, cell_size_h = {cell_size_h}, templates_path='{templates_path}'")

        self.top_left = (x, y)
        self.cell_size_w = cell_size_w
        self.cell_size_h = cell_size_h
        self.templates_path = templates_path
        self.template_images_special, self.template_images_colors, self.template_images_variants = self.get_templates()

        self.wincap = WindowCapture('Ruffle - CandyCrush.swf')
        self.set_cropped_x_y()

        #print board size
        print(f"Board size: {self.cell_size_w * 9}x{self.cell_size_h * 9}")

        print(f"Time to load templates: {time.time() - start_time}")
    
    def set_cropped_x_y(self):

        window_size = self.wincap.window_size

        cell_size_percentage = (0.09247609147609148, 0.09552599758162031)
        cell_size_w, cell_size_h = int(window_size[0] * cell_size_percentage[0]), int(window_size[1] * cell_size_percentage[1])
        
        self.cropped_x = int(cell_size_w + cell_size_w*0.58)
        self.cropped_y = int(cell_size_h + cell_size_h*0.12)

    def get_templates(self):
        candy_colors = ['blue', 'green', 'orange', 'purple', 'red', 'yellow']

        template_images_colors = {}
        template_images_variants = {}
        template_images_special = {}
        for color in candy_colors:
            template_images_colors[color] = cv2.imread(f'{self.templates_path}/{color}/{color}.png', cv2.IMREAD_UNCHANGED)

            template_images_variants[color+'_sh'] = cv2.imread(f'{self.templates_path}/{color}/{color}_sh.png', cv2.IMREAD_UNCHANGED)
            template_images_variants[color+'_sv'] = cv2.imread(f'{self.templates_path}/{color}/{color}_sv.png', cv2.IMREAD_UNCHANGED)
            template_images_variants[color+'_p'] = cv2.imread(f'{self.templates_path}/{color}/{color}_p.png', cv2.IMREAD_UNCHANGED)

        template_images_special['Special_1'] = cv2.imread(f'{self.templates_path}/Special/special.png', cv2.IMREAD_UNCHANGED)
        template_images_special['Special_2'] = cv2.imread(f'{self.templates_path}/Special/special2.png', cv2.IMREAD_UNCHANGED)
        template_images_special['Special_3'] = cv2.imread(f'{self.templates_path}/Special/special3.png', cv2.IMREAD_UNCHANGED)
        template_images_special['Special_4'] = cv2.imread(f'{self.templates_path}/Special/special4.png', cv2.IMREAD_UNCHANGED)

        return template_images_special, template_images_colors, template_images_variants

    def get_candy_matrix(self):
        start_time = time.time()

        bottom_right = (self.top_left[0] + 9 * self.cell_size_w, self.top_left[1] + 9 * self.cell_size_h)
        # im = ImageGrab.grab(bbox=(self.top_left[0], self.top_left[1], bottom_right[0], bottom_right[1]))
        # im = pyautogui.screenshot(region=(self.top_left[0], self.top_left[1], self.cell_size_w * 9, self.cell_size_h * 9))

        im_array = self.wincap.get_screenshot(self.cropped_x, self.cropped_y)

        #use array slicing on the NumPy array

        # im_array = np.asarray(im)  # Convert image to a NumPy array
        # im_array = cv2.cvtColor(im_array, cv2.COLOR_RGB2BGR)

        # cv2.imshow('screen', im_array)

        candy_matrix = np.empty((9, 9), dtype=object)
        threads = []

        for i in range(9):
            for j in range(9):
                y1, y2 = i * self.cell_size_h, (i + 1) * self.cell_size_h
                x1, x2 = j * self.cell_size_w, (j + 1) * self.cell_size_w
                cell_im = im_array[y1:y2, x1:x2]  # Use array slicing on the NumPy array

                # Convert BGR to RGB
                # cell_im_rgb = cv2.cvtColor(cell_im, cv2.COLOR_BGR2RGB)

                thread = threading.Thread(target=self.process_candy, args=(cell_im, candy_matrix, i, j))
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

        #first check the special candies
        for special, template in self.template_images_special.items():
            result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val > best_score:
                best_score = max_val
                best_match = "Ñ"
        
        # then, check the main candy color
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

    # Check if the board is moving by taking 2 screenshots and comparing them whith a threshold percentage
    def board_is_moving(self):
        im1 = ImageGrab.grab(bbox=(self.top_left[0], self.top_left[1], self.top_left[0] + 9 * self.cell_size_w, self.top_left[1] + 9 * self.cell_size_h))
        time.sleep(0.05)
        im2 = ImageGrab.grab(bbox=(self.top_left[0], self.top_left[1], self.top_left[0] + 9 * self.cell_size_w, self.top_left[1] + 9 * self.cell_size_h))

        im1_array = np.asarray(im1)
        im2_array = np.asarray(im2)

        threshold = 0.03
        difference = np.sum(np.abs(im1_array - im2_array)) 
        
        t = threshold * np.sum(im2_array)
        print(f"difference: {difference}, t: {t}")
        return difference > t

        # return not np.array_equal(im1_array, im2_array)

if __name__ == '__main__':
    # print("Running test...")
    # wincap = WindowCapture('Ruffle - CandyCrush.swf')
    pass
