# from src.Sensors.old_sensors.cv2Sensor_v1 import cv2CandySensor
from src.Sensors.cv2CandySensor import cv2CandySensor
from src.Sensors.CandyDetector_v2 import CandyDetector
from src.Sensors.bgrCandySensor import BgrCandySensor

from src.utils.GameUtils import GameActions

from src.Agents.agent_v2 import Agent

from datetime import datetime
from time import sleep
import keyboard
import cv2

def main():

    # init game actions
    actions = GameActions(
        game_path = 'src/Game/ruffle.exe',
        ruffle_path = 'src/Game/CandyCrush.swf',
        templates_main_path = 'src/candy_templates/candies'
    )

    actions.open_game(delay = 11)
    actions.skip_intro()

    max_time = 4*60 + 12
    start_time = datetime.now()

    
    # Create sensor object
    candy_sensor = cv2CandySensor(*actions.get_board_data())
    # candy_sensor = CandyDetector(*actions.get_board_data())
    # candy_sensor = BgrCandySensor(*actions.get_board_data())

    # init agent
    candy_agent = Agent() 

    # Bot loop
    while keyboard.is_pressed('q') == False:

        # Get game matrix
        # actions.pause_game() #pause game
        candy_matrix = candy_sensor.get_candy_matrix()   
        print(candy_matrix)

        # Set game matrix to agent
        candy_agent.set_game_matrix(candy_matrix)

        # Get best move and execute it
        mov_data = candy_agent.play()
        # sleep(0.01)
        # actions.pause_game() #unpause game

        if mov_data is not None:
            i, j, direction = mov_data
            actions.swap_cells(i, j, direction)        

        # Check if user wants to pause
        if keyboard.is_pressed('p'):
            print("Paused...")
            sleep(3)

        # Check if time is over
        if (datetime.now() - start_time).total_seconds() > max_time:
            print("Time out")
            break

        cv2.waitKey(1)

    cv2.destroyAllWindows()

    sleep(10)

    # Take screenshot of score
    score_im_array = candy_sensor.wincap.get_screenshot()
    cv2.imwrite(f"src/score_screenshots/score_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png", score_im_array)

    sleep(5)
    # Close game
    actions.close_game()

if __name__ == '__main__':   
    main()

# portatil juan
# x = 133, y = 87, cell_size_w = 88, cell_size_h = 78, templates_path='candies'

# pc juan
# x = 105, y = 70, cell_size_w = 71, cell_size_h = 63, templates_path='candies_pc'


