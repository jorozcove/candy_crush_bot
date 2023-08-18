import os
import cv2
import numpy as np
import pyautogui
import time

'''
Folder structure:
candies
    blue
        blue.png
        blue_p.png
        blue_sv.png
        blue_sh.png
    green
        ...
    ...
'''
#get list of all candies
candies_im = []
for folder in os.listdir('candies'):
    for file in os.listdir(os.path.join('candies', folder)):
        candies_im.append(os.path.join('candies', folder, file))

idx = candies_im.index('candies\\green\\g1.png')
threshhold = 10
#use pyautogui to find all candies in the board
for candy in candies_im[idx:idx+1]:
    positions = []
    print('Looking for', candy)

    prev_positions = list(pyautogui.locateAllOnScreen(candy, confidence=0.70, region=(top_left[0], top_left[1], 9 * cell_size_h, 9 * cell_size_v )))

    #filter out the positions that are too close to each other
    for pos in prev_positions:
        if len(positions) == 0:
            positions.append(pos)
        else:
            if min([abs(pos[0] - p[0]) for p in positions]) > threshhold or min([abs(pos[1] - p[1]) for p in positions]) > threshhold:
                positions.append(pos)


    print('Found', len(positions))
    for pos in positions:
        pyautogui.moveTo(pos[0]+40, pos[1]+40)
        pyautogui.click()
        time.sleep(0.5)