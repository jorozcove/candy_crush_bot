# from cv2CandySensor import cv2CandySensor
# from sensor2 import cv2CandySensor
from sensor2_threads import cv2CandySensor
from time import sleep

if __name__ == '__main__':
    candy_sensor = cv2CandySensor(x = 105, y = 70, cell_size_h = 71, cell_size_v = 63, templates_path='candies_pc')
    while True:
        print(candy_sensor.get_candy_matrix())
        input("Enter to continue...")

# portatil juan
# x = 133, y = 87, cell_size_h = 88, cell_size_v = 78, templates_path='candies'

# pc juan
# x = 105, y = 70, cell_size_h = 71, cell_size_v = 63, templates_path='candies_pc'
