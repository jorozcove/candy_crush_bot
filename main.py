from sensors.cv2CandySensor import cv2CandySensor
import platform
if platform.system() == 'Windows':
    from sensors.board_detector import get_board_data
else:
    from  sensors.board_detector_linux import get_board_data
from resizer import resize_images
from GameActions import GameActions

from time import sleep
import os

import subprocess

import keyboard
from agents.agent_v2 import Agent

from datetime import datetime

max_time = 4*60 + 20

def main():

    start_time = datetime.now()

    # Open game
    subprocess.Popen(["Game/ruffle.exe", "Game/CandyCrush.swf"])
    sleep(5)

    # Get board data, resize images if needed
    x, y, cell_size_w, cell_size_h = get_board_data() 
    templates_path = f'candies{cell_size_w}x{cell_size_h}'
    if not os.path.exists(templates_path):
        print(f"Resizing images to {cell_size_w}x{cell_size_h}")
        templates_path = resize_images(w = cell_size_w, h = cell_size_h)

    # Create sensor object
    candy_sensor = cv2CandySensor(x, y, cell_size_w, cell_size_h, templates_path=templates_path)

    # init game actions
    actions = GameActions(x, y, cell_size_w, cell_size_h)

    for i in range(4):
        actions.click_cell(0, 0)
        sleep(0.01)
    
    # Wait for game to load
    sleep(2)

    candy_agent = Agent() 

    while keyboard.is_pressed('q') == False:
        # if not candy_sensor.board_is_moving():     
        candy_matrix = candy_sensor.get_candy_matrix()
        print(candy_matrix)
        if candy_matrix is None:
            print("Game Ended")
            break

        candy_agent.set_game_matrix(candy_matrix)
        mov_data = candy_agent.play()
        if mov_data is not None:
            i, j, direction = mov_data
        
        actions.swap_cells(i, j, direction)

        if keyboard.is_pressed('p'):
            print("Paused...")
            sleep(3)
        # else:
        #     print("Board is moving...")
        #     sleep(0.1)

        if (datetime.now() - start_time).total_seconds() > max_time:
            print("Time out")
            break
        

if __name__ == '__main__':
    main()

# portatil juan
# x = 133, y = 87, cell_size_w = 88, cell_size_h = 78, templates_path='candies'

# pc juan
# x = 105, y = 70, cell_size_w = 71, cell_size_h = 63, templates_path='candies_pc'


