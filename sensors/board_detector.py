import win32gui

# return x, y and size of window
def get_window_data():
    window_name = 'Ruffle - CandyCrush.swf'
    hwnd = win32gui.FindWindow(None, window_name)
    if hwnd:
        win32gui.SetForegroundWindow(hwnd)
        rect = win32gui.GetWindowRect(hwnd)  
        x, y = rect[0], rect[1]
        w, h = rect[2] - x, rect[3] - y
        return x, y, w, h

    else:
        return None

def get_board_data():
    x, y, w, h = get_window_data()
    window_size = (w, h)
    cell_size_percentage = (0.09147609147609148, 0.09552599758162031)#(0.03697916666666667, 0.058333333333333334)

    cell_size_w, cell_size_h = int(window_size[0] * cell_size_percentage[0]), int(window_size[1] * cell_size_percentage[1])

    if x is None or y is None:
        raise Exception("Game window not found")

    x_board, y_board = x + int(cell_size_w + cell_size_w*0.58), y + int(cell_size_h + cell_size_h*0.12)

    return x_board, y_board, cell_size_w, cell_size_h