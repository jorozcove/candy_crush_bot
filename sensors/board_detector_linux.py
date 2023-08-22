from Xlib import display, X
import Xlib.Xutil as Xutil

def get_window_coords():
    display_var = display.Display()
    window_name = 'Ruffle - CandyCrush.swf'
    root = display_var.screen().root
    root.change_attributes(event_mask=Xlib.X.SubstructureNotifyMask)
    window_id = None
    while window_id is None:
        event = display_var.next_event()
        if event.type == X.MapNotify and event.window.get_wm_name() == window_name:
            window_id = event.window
    window_id.set_input_focus(X.RevertToParent, X.CurrentTime)
    window_id.configure(stack_mode=X.Above)
    window_id.map()
    window_geometry = window_id.get_geometry()
    return window_geometry.x, window_geometry.y

def get_board_data():
    screen_size = display.Display().screen().root.get_geometry()
    cell_size_percentage = (0.03697916666666667, 0.058333333333333334)
    cell_size_w, cell_size_h = int(screen_size.width * cell_size_percentage[0]), int(screen_size.height * cell_size_percentage[1])
    x, y = get_window_coords()
    if x is None or y is None:
        raise Exception("Game window not found")
    x_board, y_board = x + int(cell_size_w + cell_size_w*0.58), y + int(cell_size_h + cell_size_h*0.12)
    return x_board, y_board, cell_size_w, cell_size_h