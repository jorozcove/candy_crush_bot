from src.Sensors.old_sensors.cv2Sensor_v1 import cv2CandySensor
from src.Sensors.cv2CandySensor import cv2CandySensor
from src.Sensors.CandyDetector_v2 import CandyDetector
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

def debugImg(img):
    while True:
        cv2.imshow('test', img)
        if cv2.waitKey(25) & 0xFF == ord('c'):
            cv2.destroyAllWindows()
            break

def main():
    # init game actions
    game_name = 'CandyCrush.swf'#'90_ticks'

    # game_name = 'candy-crush.exe'
    use_ruffle = True

    window_name = f'Ruffle - {game_name}' if use_ruffle else 'Adobe Flash Player 10'
    
    actions = GameActions(
        game_path = f'src/Game/{game_name}',
        ruffle_path = 'src/Game/ruffle.exe',
        window_name = window_name,
        ruffle = use_ruffle
    )

    # while keyboard.is_pressed('i') == False:
    #     print("Press 'i' to start")
    #     pass
    
    # sleep(5)

    max_time = 4*60 + 12
    start_time = datetime.now()

    actions.open_game(fps = 120, delay = 5.5)

    # Create sensor object
    # candy_sensor = cv2CandySensor(*actions.get_board_data())
    # candy_sensor = CandyDetector(*actions.get_board_data())

    candy_sensor = BgrCandySensor(window_name, use_ruffle=use_ruffle)
    actions.set_board_values(*candy_sensor.get_board_data())
    actions.skip_intro()

    # init agent
    candy_agent = Agent() 

    prev_mov_data = (0, 0, 'up')

    repeated_moves = 0

    # Bot loop
    while keyboard.is_pressed('q') == False:

        # Check if user wants to pause the bot
        if keyboard.is_pressed('p'):
            print("Paused...")
            sleep(3)
        
        # Get game matrix
        # actions.pause_game() #pause game
        candy_matrix, img = candy_sensor.get_candy_matrix()
        # debugImg(img)
        actions.set_board_values(*candy_sensor.get_board_data())

        # if candy_sensor.game_is_over():
        #     print("Game over")
        #     break
          
        if not candy_sensor.board_is_moving(candy_matrix, threshold = 5):
            # Set game matrix to agent
            candy_agent.set_game_matrix(candy_matrix)

            # Get best move and execute it
            mov_data = candy_agent.play()
            
            # sleep(0.01)
            # actions.pause_game() #unpause game

            if mov_data is not None:
                if mov_data == prev_mov_data:
                    print("Movimiento repetido")
                    print(mov_data, prev_mov_data)
                    prev_mov_data = (0, 0, 'up')
                    repeated_moves += 1
                    
                else:
                    print(candy_matrix)
                    i, j, direction = mov_data
                    actions.swap_cells(i, j, direction)
                    prev_mov_data = mov_data
            
        else:
            print(candy_matrix)
            print("Board is moving...")

        # Check if time is over
        # if (datetime.now() - start_time).total_seconds() > max_time:
        #     print("Time out")
        #     break

        cv2.waitKey(1)

    print(f"Repeated moves: {repeated_moves}")
    cv2.destroyAllWindows()

    sleep(8)

    # Take screenshot of score
    score_im_array = candy_sensor.wincap.get_screenshot()
    cv2.imwrite(f"src/score_screenshots/score_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png", score_im_array)

    # Close game
    actions.close_game()

if __name__ == '__main__':   
    main()

# portatil juan
# x = 133, y = 87, cell_size_w = 88, cell_size_h = 78, templates_path='candies'

# pqqqqqqqqqqc juan
# x = 105, y = 70, cell_size_w = 71, cell_size_h = 63, templates_path='candies_pc'


