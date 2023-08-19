import os
import numpy as np
import pyautogui
import time

#NO SIRVE

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

top_left = (133, 87)
cell_size_h = 88
cell_size_v = 78
candy_colors = ['blue', 'green', 'orange', 'purple', 'red', 'yellow']

def get_cell_region(i,j):
    region = (top_left[0] + i * cell_size_h, top_left[1] + j * cell_size_v, cell_size_h, cell_size_v)
    return region

def main():
    #get list of all candies
    candy_paths = {}
    for color in candy_colors:
        candy_paths[color] = f'candies/{color}/{color}.png'
        # candy_paths[color+'_sh'] = f'candies/{color}/{color}_sh.png'
        # candy_paths[color+'_sv'] = f'candies/{color}/{color}_sv.png'
        # candy_paths[color+'_p'] = f'candies/{color}/{color}_p.png'

    # candy_paths['Ñ'] = f'candies/Special/special.png'

    #use pyautogui to find all candies in the board

    candy_matrix = np.empty((9, 9), dtype=object)
    for i in range(9):
        for j in range(9):
            print(">>>>",i,j)
            region = get_cell_region(j,i)
            region = (region[0], region[1], region[2]+1, region[3]+1)
            for variant, im_path in candy_paths.items():
                if pyautogui.locateOnScreen(im_path, grayscale=True, confidence=0.50, region=region):
                    print(variant, i, j)
                    candy_matrix[i, j] = variant[0] + ('_'+variant.split('_')[1] if '_' in variant else '')
                    break
            
            print("No candy found")
                    
                    # pyautogui.moveTo(candy[0]+40, candy[1]+40)
                    # pyautogui.click()
                    # time.sleep(0.5)

    print(candy_matrix)

if __name__ == '__main__':
    while True:
        main()
        input("Enter to continue...")











#filter out the positions that are too close to each other
# for pos in prev_positions:
#     if len(positions) == 0:
#         positions.append(pos)
#     else:
#         if min([abs(pos[0] - p[0]) for p in positions]) > threshhold or min([abs(pos[1] - p[1]) for p in positions]) > threshhold:
#             positions.append(pos)


# print('Found', len(positions))
# for pos in positions:
#     pyautogui.moveTo(pos[0]+40, pos[1]+40)
#     pyautogui.click()
#     time.sleep(0.5)