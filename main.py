# from cv2CandySensor import cv2CandySensor
from sensor2 import cv2CandySensor

if __name__ == '__main__':
    candy_sensor = cv2CandySensor()
    while True:
        print(candy_sensor.get_candy_matrix())
        input("Enter to continue...")