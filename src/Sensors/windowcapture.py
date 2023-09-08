#CODE FROM: https://github.com/learncodebygaming/opencv_tutorials/blob/master/004_window_capture/windowcapture.py

import numpy as np
import win32gui, win32ui, win32con

class WindowCapture:

    # properties
    w = 0
    h = 0
    hwnd = None
    x = 0
    y = 0

    # constructor
    def __init__(self, window_name):
        # find the handle for the window we want to capture
        self.window_hwnd = win32gui.FindWindow(None, window_name)
        if not self.window_hwnd:
            raise Exception('Window not found: {}'.format(window_name))

        # get the window size
        self.set_window_values()

    def set_window_values(self):
        window_rect = win32gui.GetWindowRect(self.window_hwnd)

        self.x = window_rect[0]
        self.y = window_rect[1]

        self.window_w = window_rect[2] - self.x
        self.window_h = window_rect[3] - self.y

        self.window_size = (self.window_w, self.window_h)

    def get_screenshot(self, x=0, y=0, w=0, h=0):
        if w == 0:
            w = self.window_w

        if h == 0:
            h = self.window_h

        # get the window image data
        wDC = win32gui.GetWindowDC(self.window_hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (w, h), dcObj, (x, y), win32con.SRCCOPY)

        # convert the raw data into a format opencv can read
        #dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (h, w, 4)

        # free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.window_hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        # drop the alpha channel, or cv.matchTemplate() will throw an error like:
        #   error: (-215:Assertion failed) (depth == CV_8U || depth == CV_32F) && type == _templ.type() 
        #   && _img.dims() <= 2 in function 'cv::matchTemplate'
        img = img[...,:3]

        # make image C_CONTIGUOUS to avoid errors that look like:
        #   File ... in draw_rectangles
        #   TypeError: an integer is required (got type tuple)
        # see the discussion here:
        # https://github.com/opencv/opencv/issues/14866#issuecomment-580207109
        img = np.ascontiguousarray(img)

        return img

    # find the name of the window you're interested in.
    # once you have it, update window_capture()
    # https://stackoverflow.com/questions/55547940/how-to-get-a-list-of-the-name-of-every-open-window
    def list_window_names(self):
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)
