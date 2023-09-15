
from src.Sensors.windowcapture import WindowCapture
import cv2

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

    return board_relative_x, board_relative_y-22, cell_size_w, cell_size_h

game_name = 'Adobe Flash Player 10'
w_name = f'{game_name}'#'Adobe Flash Player 10'

wincap = WindowCapture(w_name)

b_data = set_board_values(wincap)
print(b_data)

# cv2.namedWindow('test')
# cv2.resizeWindow('test', 500, 150)

# cv2.createTrackbar('x', 'test', 114, 150, lambda x: None)
# cv2.createTrackbar('y', 'test', 46, 150, lambda x: None)
# cv2.createTrackbar('w', 'test', 638, 1000, lambda x: None)
# cv2.createTrackbar('h', 'test', 569, 1000, lambda x: None)

while True:

    # x_offset = cv2.getTrackbarPos('x', 'test')
    # y_offset = cv2.getTrackbarPos('y', 'test')
    # w = cv2.getTrackbarPos('w', 'test')
    # h = cv2.getTrackbarPos('h', 'test')

    # img = wincap.get_screenshot(x_offset, y_offset, w, h)
    img = wincap.get_screenshot(b_data[0], b_data[1], b_data[2]*9, b_data[3]*9)

    cv2.imshow('test1', img)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

# board_relative_x = 114
# board_relative_y = 46
# board_w = 638
# board_h = 569

