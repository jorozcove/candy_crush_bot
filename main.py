from sensors.cv2CandySensor import cv2CandySensor
from sensors.board_detector import get_board_data
from resizer import resize_images
from GameActions import GameActions

from time import sleep
import os

import subprocess

def main():

    # Open game
    subprocess.Popen(["Game/ruffle.exe", "Game/CandyCrush.swf"])
    sleep(10)

    # Get board data, resize images if needed
    x, y, cell_size_w, cell_size_h = get_board_data() 
    templates_path = f'candies{cell_size_w}x{cell_size_h}'
    if not os.path.exists(templates_path):
        print(f"Resizing images to {cell_size_w}x{cell_size_h}")
        templates_path = resize_images(w = cell_size_w, h = cell_size_h)

    # Create sensor object
    candy_sensor = cv2CandySensor(x, y, cell_size_w, cell_size_h, templates_path=templates_path)

    # init game actions
    Actions = GameActions(x, y, cell_size_w, cell_size_h)
    
    # Wait for game to load
    sleep(14)

    while True:
        if not candy_sensor.board_is_moving():     
            print(candy_sensor.get_candy_matrix())
            i, j = map(int, input("Introduce i, j: ").split())
            direction = input("Introduce direction: ")
            Actions.exchange_cells(i, j, direction)
        else:
            print("Board is moving...")
            sleep(0.2)
        

if __name__ == '__main__':
    main()

# portatil juan
# x = 133, y = 87, cell_size_w = 88, cell_size_h = 78, templates_path='candies'

# pc juan
# x = 105, y = 70, cell_size_w = 71, cell_size_h = 63, templates_path='candies_pc'


