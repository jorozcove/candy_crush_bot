#include parent folder in path
import sys
sys.path.append("..")

from time import sleep
from .resizer import resize_images
import os
import subprocess
import keyboard
from pynput.mouse import Button, Controller

import win32api, win32con

import pygetwindow as gw

class GameActions:
    def __init__(self, game_path, ruffle_path, window_name, game_engine, x_offset = 0, y_offset = 0):
        self.game_path = game_path
        self.ruffle_path = ruffle_path
        self.window_name = window_name
        self.game_engine = game_engine
        self.x_offset = x_offset
        self.y_offset = y_offset

        launch_params = {
            'ruffle': [self.ruffle_path, self.game_path, '--frame-rate', '60', '--open-url-mode', 'deny'],
            'flash_exe': [self.game_path],
            'flash_stand_alone': ['src/Game/flashplayer_32_sa.exe',self.game_path]
        }

        self.launch_params = launch_params[game_engine]

        self.mouse = Controller()

    def open_game(self, fps = '60', delay = 8):
        if self.game_engine == 'ruffle':
            self.launch_params[3] = str(fps)

        print(self.launch_params)
        subprocess.Popen(self.launch_params)

        window = gw.getWindowsWithTitle(self.window_name)
        while not window:
            window = gw.getWindowsWithTitle(self.window_name)
        
        window = window[0]
        window.moveTo(0, 0)

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

    def skip_intro(self, delay = 2):
        for _ in range(4):
            self.click_cell(0, 0)
            sleep(0.01)
        # Wait for game to begin
        sleep(delay)

    def pause_game(self):
        # Pause game
        keyboard.press_and_release('a')

    def close_game(self):
        # Close game
        if self.game_engine == 'ruffle':
            subprocess.Popen(['taskkill', '/F', '/IM', 'ruffle.exe'])
        elif self.game_engine == 'flash_exe':
            subprocess.Popen(['taskkill', '/F', '/IM', 'candy-crush.exe'])
        elif self.game_engine == 'flash_stand_alone':
            subprocess.Popen(['taskkill', '/F', '/IM', 'flashplayer_32_sa.exe'])

    def click(self, x, y):
        # win32api.SetCursorPos((x, y))
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        # sleep(0.02)
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        
        # pyautogui.moveTo(x + self.x_offset, y + self.y_offset)
        # pyautogui.click()

        self.mouse.position = (x + self.x_offset, y + self.y_offset)
        self.mouse.press(Button.left)
        self.mouse.release(Button.left)
        

    def click_cell(self, cell_i, cell_j):
        data = self.x + self.cell_size_w * cell_j + self.cell_size_w // 2, self.y + self.cell_size_h * cell_i + self.cell_size_h // 2
        print(cell_i, cell_j, data)
        self.click(*data)

    def swap_cells(self, cell_i, cell_j, direction):
        if direction == 'up':
            self.click_cell(cell_i, cell_j)
            sleep(0.05)
            self.click_cell(cell_i - 1, cell_j)

        elif direction == 'down':
            self.click_cell(cell_i, cell_j)
            sleep(0.05)
            self.click_cell(cell_i + 1, cell_j)

        elif direction == 'left':
            self.click_cell(cell_i, cell_j)
            sleep(0.05)
            self.click_cell(cell_i, cell_j - 1)

        elif direction == 'right':
            self.click_cell(cell_i, cell_j)
            sleep(0.05)
            self.click_cell(cell_i, cell_j + 1)

if __name__ == "__main__":
    pass