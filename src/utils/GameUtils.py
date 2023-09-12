#include parent folder in path
import sys
sys.path.append("..")

import win32api
import win32con
from time import sleep
from .resizer import resize_images
import os
import subprocess
import keyboard
import pyautogui

class GameActions:
    def __init__(self, game_path, ruffle_path):
        self.game_path = game_path
        self.ruffle_path = ruffle_path

    def open_game(self, fps = '60', delay = 8):
        # Open game ruffle.exe CandyCrush.swf --frame-rate 100 --open-url-mode deny
        subprocess.Popen([self.ruffle_path, self.game_path, '--frame-rate', str(fps), '--open-url-mode', 'deny'])

        # Wait for game to load
        sleep(delay)
    
    def set_board_values(self, x, y, cell_size_w, cell_size_h):
        self.x = x
        self.y = y
        self.cell_size_w = cell_size_w
        self.cell_size_h = cell_size_h
        
    def resize_images(self, templates_main_path):
        templates_path = os.path.join(os.getcwd(), f'{templates_main_path}{cell_size_w}x{cell_size_h}')
        if not os.path.exists(templates_path):
            print(f"Resizing images to {cell_size_w}x{cell_size_h}")
            templates_path = resize_images(w = cell_size_w, h = cell_size_h, path = self.templates_main_path)
        self.templates_path = templates_path

    def skip_intro(self):
        for _ in range(4):
            self.click_cell(0, 0)
            sleep(0.01)
        # Wait for game to begin
        sleep(2)

    def pause_game(self):
        # Pause game
        keyboard.press_and_release('a')

    def close_game(self):
        # Close game
        subprocess.Popen(['taskkill', '/F', '/IM', 'ruffle.exe'])

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
