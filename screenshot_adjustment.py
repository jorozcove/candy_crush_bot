
from src.Sensors.windowcapture import WindowCapture
import cv2
# import pyautogui
from src.Sensors.bgrCandySensor import BgrCandySensor

def set_board_values(wincap):
    wincap.set_window_values()
    window_size = wincap.window_size
    print(f"WINDOW SIZE: {window_size}")

    cell_size_percentage = (0.09247609147609148, 0.09552599758162031)
    cell_size_w, cell_size_h = int(window_size[0] * cell_size_percentage[0]), int(window_size[1] * cell_size_percentage[1])
    
    board_relative_x = int(cell_size_w + cell_size_w*0.58)
    board_relative_y = int(cell_size_h + cell_size_h*0.12)

    board_x = board_relative_x + wincap.x
    board_y = board_relative_y + wincap.y

    cell_size_w = cell_size_w
    cell_size_h = cell_size_h

    return board_relative_x, board_relative_y, cell_size_w, cell_size_h

game_name = 'Adobe Flash Player 32' #'Ruffle - CandyCrush.swf'
w_name = f'{game_name}'

wincap = WindowCapture(w_name)

b_data = set_board_values(wincap)
print(b_data)

cv2.namedWindow('test')
cv2.resizeWindow('test', 500, 200)

cv2.createTrackbar('x', 'test', 114, 150, lambda x: None)
cv2.createTrackbar('y', 'test', 46, 150, lambda x: None)
cv2.createTrackbar('w', 'test', 638, 1000, lambda x: None)
cv2.createTrackbar('h', 'test', 569, 1000, lambda x: None)
cv2.createTrackbar('y_offset', 'test', 19, 100, lambda x: None)

candy_sensor = BgrCandySensor(w_name)

mode = 'slice'

while True:

    #change mode with m
    if cv2.waitKey(25) & 0xFF == ord('m'):
        if mode == 'slice':
            mode = 'candy'
            print('candy mode')
        else:
            mode = 'slice'
            print('slice mode')

    if mode == 'slice':
        x_offset = cv2.getTrackbarPos('x', 'test')
        y_offset = cv2.getTrackbarPos('y', 'test')
        w = cv2.getTrackbarPos('w', 'test')
        h = cv2.getTrackbarPos('h', 'test')

        # img = wincap.get_screenshot(x_offset, y_offset, w, h)
        y_offset_2 = cv2.getTrackbarPos('y_offset', 'test')
        img = wincap.get_screenshot(b_data[0], b_data[1]-y_offset_2, b_data[2]*9, b_data[3]*9)
        
        cv2.imshow('test1', img)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
    
    else:
        #wait until c is pressed
        while True:
            if cv2.waitKey(25) & 0xFF == ord('c'):
                break
                #change mode with m
            if cv2.waitKey(25) & 0xFF == ord('m'):
                if mode == 'slice':
                    mode = 'candy'
                    print('candy mode')
                else:
                    mode = 'slice'
                    print('slice mode')
                
                break
            
        candy_matrix, img = candy_sensor.get_candy_matrix_img(img)
        print(candy_matrix)

    
        

    

# board_relative_x = 114
# board_relative_y = 46
# board_w = 638
# board_h = 569

