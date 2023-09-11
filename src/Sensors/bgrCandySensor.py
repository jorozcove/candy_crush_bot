from .windowcapture import WindowCapture
import numpy as np

from time import sleep
from datetime import datetime
import cv2

def debugImg(img):
    while True:
        cv2.imshow('test', img)
        if cv2.waitKey(25) & 0xFF == ord('c'):
            cv2.destroyAllWindows()
            break

class BgrCandySensor:
    def __init__(self, window_name):

        self.colors_bgr = { 
          "r": (1, 2, 246), "r_sh": (59,  59, 236), "r_sv": (78,  80, 237), "r_p": (36, 35, 253),
          "g" : (2, 181, 54), "g_sh": ( 74, 233, 111), "g_sv": (107, 242, 143), "g_p": (47, 229, 91),
          "b": (252, 152,  46), "b_sh": (236, 186,  75), "b_sv": (246, 196, 109),"b_p": (254, 190,  37),
          "y": (12, 225, 252),  "y_sh": (96, 226, 251), "y_sv": (94, 224, 252), "y_p": (51, 225, 255),
          "p": (255,  37, 199), "p_sh": (243,  92, 217), "p_sv": (245, 102, 217), "p_p": (255,  40, 206),
          "o": (35, 155, 255), "o_sh" : (94, 192, 249), "o_sv": (102, 197, 248), "o_p" : (30, 170, 255),
          "Ñ": (45, 69, 112)
         }

        # self.colors_bgr = { 
        #   "r": (1, 2, 246), "r_sh": (72,  74, 243), "r_sv": (99, 102, 246), "r_p": (36, 35, 253),
        #   "g" : (2, 181, 54), "g_sh": ( 62, 225, 101), "g_sv": (79, 228, 116), "g_p": (47, 229, 91),
        #   "b": (252, 152,  46), "b_sh": (236, 186,  75), "b_sv": (244, 183,  79),"b_p": (254, 190,  37),
        #   "y": (12, 225, 252),  "y_sh": (66, 217, 251), "y_sv": (67, 216, 251), "y_p": (51, 225, 255),
        #   "p": (255,  37, 199), "p_sh": (243, 102, 217), "p_sv": (245, 102, 217), "p_p": (255,  40, 206),
        #   "o": (35, 155, 255), "o_sh" : (112, 197, 249), "o_sv": (129, 207, 250), "o_p" : (30, 170, 255),
        #   "Ñ": (45, 69, 112)
        #  }
        
        self.wincap = WindowCapture(window_name)
        self.set_board_values()
    
    def set_board_values(self):
        self.wincap.set_window_values()
        window_size = self.wincap.window_size

        cell_size_percentage = (0.09247609147609148, 0.09552599758162031)
        cell_size_w, cell_size_h = int(window_size[0] * cell_size_percentage[0]), int(window_size[1] * cell_size_percentage[1])
        
        self.board_relative_x = int(cell_size_w + cell_size_w*0.58)
        self.board_relative_y = int(cell_size_h + cell_size_h*0.12)

        self.board_x = self.board_relative_x + self.wincap.x
        self.board_y = self.board_relative_y + self.wincap.y

        self.cell_size_w = cell_size_w
        self.cell_size_h = cell_size_h

    def get_board_data(self):
        return self.board_x, self.board_y, self.cell_size_w, self.cell_size_h

    def bgr_mean(self, bgr_img):
        color_mean = np.average(bgr_img, axis = 0)
        color_mean = np.average(color_mean, axis = 0)
        color_mean = np.uint8([[color_mean]])
        return color_mean[0][0]

    # get mean BGR color value of candy at position r,c in gameboard
    # returns as (b,g,r) set
    def get_bgr_mean(self, r,c,img):
        x = (self.cell_size_w//2 + c * self.cell_size_w) - 10 # 10
        y = (self.cell_size_h//2 + r * self.cell_size_h) - 10 # 10
        bgr_img = img[y:y+20, x:x+20]

        mean_px = self.bgr_mean(bgr_img)
        return mean_px
    
    # categorize [color] into one from COLORS_BGR using manhattan distances
    # if distance is above a threshold, returns '?'
    def categorize_color(self, bgr_tuple):
        manhattan = lambda x,y : abs(x[0] - y[0]) + abs(x[1] - y[1]) + abs(x[2] - y[2])
        distances = {k: manhattan(v, bgr_tuple) for k, v in self.colors_bgr.items()}
        color = min(distances, key=distances.get)
        threshold = 90 #40
        if not distances[color] > threshold:
            return color
        return '?'
    
    #Check if board is moving by counting the number of '?' in the candy_matrix
    def board_is_moving(self, candy_matrix, threshold = 1):
        return np.count_nonzero(candy_matrix == '?') > threshold
    
    def get_color(self, i, j):
        image = self.wincap.get_screenshot(self.board_relative_x, self.board_relative_y, self.cell_size_w*9, self.cell_size_h*9)
        colorVal = self.get_bgr_mean(i, j, image)
        colorName = self.categorize_color(colorVal)

        return colorVal, colorName
    
    #check if game is over by checking if there is the close button in the bottom left corner
    def game_is_over(self):

        img = self.wincap.get_screenshot(
            x = 0,
            y = self.board_relative_y + int(8.6 * self.cell_size_h),
            w = int(self.cell_size_w * 0.6),
            h = int(self.cell_size_h * 1.5)
        )
        
        close_bttn_bgr = (25, 27, 52)
        bgr_mean = self.bgr_mean(img)

        # compare distance between bgr_mean and close_bttn_bgr
        manhattan = lambda x,y : abs(x[0] - y[0]) + abs(x[1] - y[1]) + abs(x[2] - y[2])

        distance = manhattan(bgr_mean, close_bttn_bgr)

        print("...............",distance)
    # debugImg(img)

        return distance > 60

    # Read pixel colors from game screen and initialize candy_matrix
    def get_candy_matrix(self):
        start_time = datetime.now()
        self.set_board_values()

        candy_matrix = np.empty((9, 9), dtype=object)

        image = self.wincap.get_screenshot(self.board_relative_x, self.board_relative_y, self.cell_size_w*9, self.cell_size_h*9)
        for r in range(9):
            for c in range(9):
                color_val = self.get_bgr_mean(r, c, image)
                color = self.categorize_color(color_val)
                candy_matrix[r, c] = color

        #change 0,3 to '?' because object is permanently there
        candy_matrix[0, 3] = '?'

        print(f"Time to get candy matrix: {(datetime.now() - start_time).total_seconds()} seconds")

        return candy_matrix, image