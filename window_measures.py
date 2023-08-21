from win32api import GetSystemMetrics

screen_size = (GetSystemMetrics(0), GetSystemMetrics(1))
print(screen_size)

cell_size_percentage = (0.03697916666666667, 0.058333333333333334)

cell_size = (int(screen_size[0] * cell_size_percentage[0]), int(screen_size[1] * cell_size_percentage[1]))
print(cell_size)

top_left_board_percentage = (0.0546875, 0.06481481481481481)

top_left_board = (int(screen_size[0] * top_left_board_percentage[0]), int(screen_size[1] * top_left_board_percentage[1]))
print(top_left_board)