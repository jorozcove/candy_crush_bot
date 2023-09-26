# from src.Sensors.old_sensors.cv2Sensor_v1 import cv2CandySensor
# from src.Sensors.cv2CandySensor import cv2CandySensor
# from src.Sensors.CandyDetector_v2 import CandyDetector
from src.Sensors.bgrCandySensor import BgrCandySensor

from src.utils.GameUtils import GameActions

# from src.Agents.agent import Agent
# from src.Agents.agent_v2 import Agent
from src.Agents.agent_v3 import Agent

from datetime import datetime
from time import sleep
import keyboard
import cv2

import numpy as np

GAME_FILENAME = 'CandyCrush.swf'
# GAME_FILENAME = '90_ticks.swf' 
# GAME_FILENAME = '300_ticks.swf'
# GAME_FILENAME = '1000_ticks.swf'
# GAME_FILENAME = 'candy-crush.exe'

# ENGINE_FILENAME = 'ruffle'
# ENGINE_FILENAME = 'flash_exe'
ENGINE_FILENAME = 'flash_stand_alone'

RUFFLE_FPS = 120
OPEN_DELAY = 5
SKIP_DELAY = 1
MOVING_THRESHOLD = 5
CATEGORIZE_THRESHOLD = 90
OPEN_GAME = True

def main():

    candy_actions, candy_sensor, candy_agent = init_bot(GAME_FILENAME, ENGINE_FILENAME, OPEN_GAME = OPEN_GAME)

    prev_mov_data = (0, 0, 'up') # set an invalid move
    repeated_moves = 0

    # Bot loop
    while True:
        ################# BOT CONTROLS #################

        # Quit bot
        key = 'q'
        if keyboard.is_pressed(key):
            break

        # Quit and close game
        key = 'x'
        if keyboard.is_pressed(key):
            candy_actions.close_game()
            break

        #restart bot
        key = 'ñ'
        if keyboard.is_pressed(key):
            candy_actions.close_game()
            sleep(1)
            cv2.destroyAllWindows()
            main()
            return 0

        # Pause game and bot
        key = 'p'
        if keyboard.is_pressed(key):
            print("Paused...")
            pause_bot(candy_actions, key, pause_game=True)
            print("Unpaused...")
        
        # Pause bot only
        key = 'o'
        if keyboard.is_pressed(key):
            print("Paused...")
            pause_bot(candy_actions, key, pause_game=False)
            print("Unpaused...")

        # Pause game only (Press 'a')

        # if candy_sensor.game_is_over():
        #     print("Game over")
        #     break

        ################# BOT LOGIC #################
        
        # Get game matrix
        candy_matrix, img = candy_sensor.get_candy_matrix()
        candy_actions.set_board_values(*candy_sensor.get_board_data())
          
        if not candy_sensor.board_is_moving(candy_matrix, threshold = MOVING_THRESHOLD):
            # Set game matrix to agent
            candy_agent.set_game_matrix(candy_matrix)

            # Get best move and execute it
            mov_data = candy_agent.play()

            if mov_data is not None:
                if mov_data == prev_mov_data:
                    # print("Movimiento repetido")
                    # print(mov_data, prev_mov_data)
                    prev_mov_data = (0, 0, 'up')
                    repeated_moves += 1
                    
                else:
                    # print(candy_matrix)
                    i, j, direction = mov_data
                    candy_actions.swap_cells(i, j, direction)
                    prev_mov_data = mov_data
            
        cv2.waitKey(1)

    print(f"Repeated moves: {repeated_moves}")
    cv2.destroyAllWindows()

    # sleep(8)

    # # Take screenshot of score
    # score_im_array = candy_sensor.wincap.get_screenshot()
    # cv2.imwrite(f"src/score_screenshots/score_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png", score_im_array)

    # # Close game
    # candy_actions.close_game()

def pause_bot(candy_actions, key, pause_game = True):
    if pause_game: candy_actions.pause_game()
    sleep(0.6)
    while keyboard.is_pressed(key) == False:
        sleep(0.1)

    if pause_game: candy_actions.pause_game()


def init_bot(GAME_FILENAME, ENGINE_FILENAME, OPEN_GAME = True):
    window_names = {
        'ruffle': f'Ruffle - {GAME_FILENAME}',
        'flash_exe': 'Adobe Flash Player 10',
        'flash_stand_alone': 'Adobe Flash Player 32'
    }

    window_name = window_names[ENGINE_FILENAME]

    y_offset = 0
    if ENGINE_FILENAME == 'flash_exe' or ENGINE_FILENAME == 'flash_stand_alone':
        y_offset = -19

    candy_actions = GameActions(
        game_path = f'src/Game/{GAME_FILENAME}',
        ruffle_path = 'src/Game/ruffle.exe',
        window_name = window_name,
        game_engine = ENGINE_FILENAME,
        y_offset = y_offset,      
    )

    if OPEN_GAME:
        candy_actions.open_game(fps = RUFFLE_FPS, delay = OPEN_DELAY)

    # Create sensor object
    # candy_sensor = cv2CandySensor(*candy_actions.get_board_data())
    # candy_sensor = CandyDetector(*candy_actions.get_board_data())

    candy_sensor = BgrCandySensor(
        window_name,
        categorize_threshold = CATEGORIZE_THRESHOLD,
        y_offset=y_offset
    )
    candy_actions.set_board_values(*candy_sensor.get_board_data())

    if OPEN_GAME:
        candy_actions.skip_intro(delay = SKIP_DELAY)

    # keyboard.press_and_release('f')

    # init agent
    candy_agent = Agent()

    return candy_actions, candy_sensor, candy_agent

if __name__ == '__main__':   
    main()

# portatil juan
# x = 133, y = 87, cell_size_w = 88, cell_size_h = 78, templates_path='candies'

# pc juan
# x = 105, y = 70, cell_size_w = 71, cell_size_h = 63, templates_path='candies_pc'


