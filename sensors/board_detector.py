from win32api import GetSystemMetrics
import win32gui
import win32con

def get_window_coords():
    window_name = 'Ruffle - CandyCrush.swf'
    hwnd = win32gui.FindWindow(None, window_name)
    if hwnd:
        win32gui.SetForegroundWindow(hwnd)
        rect = win32gui.GetWindowRect(hwnd)  
        return rect[0], rect[1]
    else:
        return None

def get_board_data():
    screen_size = (GetSystemMetrics(0), GetSystemMetrics(1))

    cell_size_percentage = (0.03697916666666667, 0.058333333333333334)
    cell_size_w, cell_size_h = int(screen_size[0] * cell_size_percentage[0]), int(screen_size[1] * cell_size_percentage[1])

    x, y = get_window_coords()

    if x is None or y is None:
        raise Exception("Game window not found")

    x_board, y_board = x + int(cell_size_w + cell_size_w*0.58), y + int(cell_size_h + cell_size_h*0.12)

    return x_board, y_board, cell_size_w, cell_size_h