import cv2
import numpy as np
import time
import pyscreenshot as ImageGrab

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

    def get_candy_matrix(self):

        start_time = time.time()

        bottom_right = (self.top_left[0] + 9 * self.cell_size_w, self.top_left[1] + 9 * self.cell_size_h)
        board_im = ImageGrab.grab(bbox=(self.top_left[0], self.top_left[1], bottom_right[0], bottom_right[1]))

        board_im_array = cv2.cvtColor(np.asarray(board_im), cv2.COLOR_BGR2RGB)  # Convert the PIL image to a NumPy array
    
        #show image
        # cv2.imshow('board', board_im_array)
        # cv2.waitKey(0)

        candy_matrix = np.empty((9, 9), dtype=object)

        for candy_img, color, threshold in zip(
            self.templates_colors.values(),
            self.candy_colors.keys(),
            self.candy_colors.values(),
        ):

            result = cv2.matchTemplate(
                board_im_array, candy_img, cv2.TM_CCOEFF_NORMED
            )

            rectangles = []
            loc = np.where(result >= threshold)
            for pt in zip(*loc[::-1]):  # Switch columns and rows
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

        print(f"Time to get candy matrix: {time.time() - start_time}")

        return candy_matrix

if __name__ == "__main__":
    pass

