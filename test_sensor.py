from src.Sensors.bgrCandySensor import BgrCandySensor
from src.utils.GameUtils import GameActions
import cv2

import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def debugImg(img):
    while True:
        cv2.imshow('test', img)
        if cv2.waitKey(25) & 0xFF == ord('c'):
            cv2.destroyAllWindows()
            break

# actions = GameActions(
#     game_path = 'src/Game/ruffle.exe',
#     ruffle_path = 'src/Game/CandyCrush.swf',
#     templates_main_path = 'src/candy_templates/candies'
# )

game_name = 'candy-crush.exe'
use_ruffle = False

window_name = f'Ruffle - {game_name}' if use_ruffle else 'Adobe Flash Player 10'

actions = GameActions(
    game_path = f'src/Game/{game_name}',
    ruffle_path = 'src/Game/ruffle.exe',
    window_name = window_name,
    ruffle = use_ruffle
)

# actions.open_game(delay = 11)
# actions.skip_intro()

candy_sensor = BgrCandySensor(window_name, use_ruffle=use_ruffle)

candy_matrix, image = candy_sensor.get_candy_matrix()

while cv2.waitKey(1) != ord('q'):

    opt = input(">>")
    if (opt == 'a'):
        candy_matrix, image = candy_sensor.get_candy_matrix()
        print(candy_matrix)
        debugImg(image) 

    # elif (opt == 's'):
    #     #get sceenshot of score
    #     img = candy_sensor.wincap.get_screenshot(cropped_x= candy_sensor.cropped_x - int(1.27 * candy_sensor.cell_size_w),
    #                                             cropped_y = candy_sensor.cropped_y - int(-0.75 * candy_sensor.cell_size_h),
    #                                             cropped_w = int(candy_sensor.cell_size_w *1.1),
    #                                             cropped_h = int(candy_sensor.cell_size_h *0.28)
    #                                             )
    #     #to grayscale
    #     # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #     # debugImg(img)
    #     print(pytesseract.image_to_string(img, config=r'--oem 3 --psm 11 -c tessedit_char_whitelist=0123456789'))

    elif (opt == 'k'):
        #get sceenshot of bottom left corner
        # img = candy_sensor.wincap.get_screenshot(cropped_x = 0,
        #                                         cropped_y = candy_sensor.cropped_y + int(8.6 * candy_sensor.cell_size_h),
        #                                         cropped_w = int(candy_sensor.cell_size_w * 0.6),
        #                                         cropped_h = int(candy_sensor.cell_size_h * 1.5)
        #                                         )
        
        # close_bttn_bgr = (25, 27, 52)
        # bgr_mean = candy_sensor.bgr_mean(img)

        # # compare distance between bgr_mean and close_bttn_bgr
        # manhattan = lambda x,y : abs(x[0] - y[0]) + abs(x[1] - y[1]) + abs(x[2] - y[2])

        # distance = manhattan(bgr_mean, close_bttn_bgr)

        # print(distance)
        # debugImg(img) 

        #Get screenshot of position (i,j) in gameboard
        # i, j = map(int, input("i j: ").split())
        img = candy_sensor.wincap.get_screenshot(
        #     cropped_x = candy_sensor.cropped_x + j * candy_sensor.cell_size_w,
        #     cropped_y = candy_sensor.cropped_y + i * candy_sensor.cell_size_h,
        #     cropped_w = candy_sensor.cell_size_w,
        #     cropped_h = candy_sensor.cell_size_h
        )
        debugImg(img)


    else:
        i, j = map(int, opt.split())
        print(candy_sensor.get_color(i, j))

        #crop image
        x = (candy_sensor.cell_size_w//2 + j * candy_sensor.cell_size_w) - 10 # 10
        y = (candy_sensor.cell_size_h//2 + i * candy_sensor.cell_size_h) - 10 # 10
        bgr_img = image[y:y+20, x:x+20]
        debugImg(bgr_img)
