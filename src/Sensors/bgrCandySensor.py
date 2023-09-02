import cv2
import pyautogui
from .windowcapture import WindowCapture
import numpy as np


class BgrCandySensor:
    def __init__(self, x, y, cell_size_w, cell_size_h, templates_path):
        self.snapshot_area = {
            'top': y,
            'left': x,
            'width': cell_size_w * 9,
            'height': cell_size_h * 9
        }

        self.cell_size_w = cell_size_w
        self.cell_size_h = cell_size_h

        self.colors_bgr = {
          "Red": (1, 2, 246), "RS": (67, 70, 243), "RS2": (97, 101, 247), "RW": (36, 35, 253),
          "Green" : (2, 181, 54), "GS": (72, 237, 109), "GS2": (126, 244, 163), "GS3": (107, 242, 143), "GW": (47, 229, 91),
          "Blue": (255, 154, 44), "BS": (244, 205,  85), "BW": (255, 196,  36),
          "Yellow": (12, 225, 252), "YS": (76, 221, 250),
          "Purple": (255,  35, 195), "PS": (245, 107, 215),
          "Orange": (35, 155, 255), "OS": (119, 203, 249),
          "Colored": (45, 69, 112)
         }
        
        self.wincap = WindowCapture('Ruffle - CandyCrush.swf')

    def meanBgr(self, bgr_img):
        color_mean = np.average(bgr_img, axis = 0)
        color_mean = np.average(color_mean, axis = 0)
        color_mean = np.uint8([[color_mean]])
        return color_mean[0][0]

    # get mean BGR color value of candy at position r,c in gameboard
    # returns as (b,g,r) set
    def getCandyColor(self, r,c,img):
        x = (self.cell_size_w//2 + (c-1) * self.cell_size_w) - 10
        y = (self.cell_size_h//2 + (r-1) * self.cell_size_h) - 10
        bgr_img = img[y:y+20, x:x+20]
        mean_px = self.meanBgr(bgr_img)
        return mean_px
    
    # categorize [color] into one from COLORS_BGR using manhattan distances
    # if distance is above a threshold, returns '?'
    def categorizeColor(self, bgr_tuple):
        manhattan = lambda x,y : abs(x[0] - y[0]) + abs(x[1] - y[1]) + abs(x[2] - y[2])
        distances = {k: manhattan(v, bgr_tuple) for k, v in self.colors_bgr.items()}
        color = min(distances, key=distances.get)
        threshold = 40
        if not distances[color] > threshold:
            return color[0]
        return '?'

    # Read pixel colors from game screen and initialize candy_matrix
    def get_candy_matrix(self):
        candy_matrix = np.empty((9, 9), dtype=object)

        image = self.wincap.get_screenshot()
        # image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
        for r in range(9):
            for c in range(9):
                colorVal = self.getCandyColor(r+1, c+1, image)
                colorName = self.categorizeColor(colorVal)
                candy_matrix[r, c] = colorName

        return candy_matrix