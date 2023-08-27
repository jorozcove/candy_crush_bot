import cv2
import numpy as np
import time
import pyscreenshot as ImageGrab
import threading
import pyautogui

from windowcapture import WindowCapture

class CandyDetector:
    def __init__(self, x, y, cell_size_w, cell_size_h, templates_path):
        self.templates_path = templates_path
        self.cell_size_w = cell_size_w
        self.cell_size_h = cell_size_h
        self.top_left = (x, y)
        self.candy_colors = {
            'blue': 0.65,
            'green': 0.55,
            'orange': 0.83,
            'purple': 0.7,
            'red': 0.8,
            'yellow': 0.85
        }
        self.templates_colors = self.get_templates()

        self.wincap = WindowCapture('Ruffle - CandyCrush.swf')

    def to_board_i_j(self, center_x, center_y):
        i = int(center_y / self.cell_size_h)
        j = int(center_x / self.cell_size_w)
        return i, j

    def get_templates(self):
        template_images_colors = {}
        for color in self.candy_colors.keys():
            template_images_colors[color] = cv2.imread(
                f'{self.templates_path}/{color}/{color}.png', cv2.IMREAD_UNCHANGED
            )
        return template_images_colors

    def detect_candies_in_region(self, color, candy_img, threshold, board_im_array, candy_matrix):
        result = cv2.matchTemplate(board_im_array, candy_img, cv2.TM_CCOEFF_NORMED)
        rectangles = []
        loc = np.where(result >= threshold)
        for pt in zip(*loc[::-1]):
            rect = [pt[0], pt[1], candy_img.shape[1], candy_img.shape[0]]
            rectangles.append(rect)
            rectangles.append(rect)

        rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

        for rect in rectangles:
            center_x = rect[0] + rect[2] // 2
            center_y = rect[1] + rect[3] // 2
            i, j = self.to_board_i_j(center_x, center_y)
            candy_matrix[i, j] = (
                color[0] + ("_" + color.split("_")[1] if "_" in color else "")
            )

            #draw rectangle on image depending on color
            rgb_colors = {
                'blue': (255, 0, 0),
                'green': (0, 255, 0),
                'orange': (0, 165, 255),
                'purple': (255, 0, 255),
                'red': (0, 0, 255),
                'yellow': (0, 255, 255)
            }

            cv2.rectangle(board_im_array, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), rgb_colors[color], 2)


    def get_candy_matrix(self):
        start_time = time.time()
        bottom_right = (self.top_left[0] + 9 * self.cell_size_w, self.top_left[1] + 9 * self.cell_size_h)
        # board_im = ImageGrab.grab(bbox=(self.top_left[0], self.top_left[1], bottom_right[0], bottom_right[1]))
        # board_im = pyautogui.screenshot(region=(self.top_left[0], self.top_left[1], self.cell_size_w * 9, self.cell_size_h * 9))

        board_im_array = self.wincap.get_screenshot()
        
        # board_im_array = cv2.cvtColor(np.asarray(board_im), cv2.COLOR_BGR2RGB)

        # cv2.imshow('board', board_im_array)

        candy_matrix = np.empty((9, 9), dtype=object)
        threads = []

        for color, candy_img in self.templates_colors.items():
            threshold = self.candy_colors[color]
            thread = threading.Thread(target=self.detect_candies_in_region, args=(color, candy_img, threshold, board_im_array, candy_matrix))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        cv2.imshow('board', board_im_array)


        print(f"Time to get candy matrix: {time.time() - start_time}")

        return candy_matrix
if __name__ == "__main__":
    pass

