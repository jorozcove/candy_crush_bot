import win32api
import win32con
from time import sleep

import pyautogui

class GameActions:
    def __init__(self, x, y, cell_size_w, cell_size_h):
        self.x = x
        self.y = y
        self.cell_size_w = cell_size_w
        self.cell_size_h = cell_size_h

    def click(self, x, y):
        # win32api.SetCursorPos((x, y))
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        # # sleep(0.02)
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        pyautogui.moveTo(x, y)
        pyautogui.click()

    def click_cell(self, cell_i, cell_j):
        data = self.x + self.cell_size_w * cell_j + self.cell_size_w // 2, self.y + self.cell_size_h * cell_i + self.cell_size_h // 2
        print(cell_i, cell_j, data)
        self.click(*data)

    def swap_cells(self, cell_i, cell_j, direction):
        if direction == 'up':
            self.click_cell(cell_i, cell_j)
            # sleep(0.05)
            self.click_cell(cell_i - 1, cell_j)

        elif direction == 'down':
            self.click_cell(cell_i, cell_j)
            # sleep(0.05)
            self.click_cell(cell_i + 1, cell_j)

        elif direction == 'left':
            self.click_cell(cell_i, cell_j)
            # sleep(0.05)
            self.click_cell(cell_i, cell_j - 1)

        elif direction == 'right':
            self.click_cell(cell_i, cell_j)
            # sleep(0.05)
            self.click_cell(cell_i, cell_j + 1)