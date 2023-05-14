import win32api
import win32con
import win32gui


def get_windows():
    win_info = []
    excluded_apps = ['Microsoft Text Input Application', 'Параметры', 'Settings', 'One click app']

    def is_real_window(hWnd):
        """Return True iff given window is a real Windows application window."""
        if not win32gui.IsWindowVisible(hWnd):
            return False
        if win32gui.GetParent(hWnd) != 0:
            return False
        if win32gui.IsIconic(hWnd):
            return False
        has_no_owner = win32gui.GetWindow(hWnd, win32con.GW_OWNER) == 0
        lExStyle = win32gui.GetWindowLong(hWnd, win32con.GWL_EXSTYLE)
        if (((lExStyle & win32con.WS_EX_TOOLWINDOW) == 0 and has_no_owner)
                or ((lExStyle & win32con.WS_EX_APPWINDOW != 0) and not has_no_owner)):
            window_text = win32gui.GetWindowText(hWnd)
            if window_text:
                return True
        return False

    def callback(hWnd, windows):
        if not is_real_window(hWnd):
            return
        rect = win32gui.GetWindowRect(hWnd)
        window_text = win32gui.GetWindowText(hWnd)
        if window_text and window_text not in excluded_apps:
            windows.append(hWnd)  # windows.append((window_text, hWnd, (rect[2] - rect[0], rect[3] - rect[1])))
            win_info.append((window_text, hWnd, (rect[2] - rect[0], rect[3] - rect[1])))

    windows = []
    win32gui.EnumWindows(callback, windows)
    print(win_info)
    return windows, win_info


def align_windows():
    try:
        # get all windows
        windows, win_info = get_windows()
        print(windows)
        print(win_info)
        num_windows = len(windows)

        if num_windows == 0:
            print("No running applications found")
            return

        # grid size
        if num_windows <= 2:
            grid_size = (1, 2)
        elif num_windows <= 4:
            grid_size = (2, 2)
        elif num_windows <= 6:
            grid_size = (2, 3)
        elif num_windows <= 9:
            grid_size = (3, 3)
        else:
            grid_size = (3, 4)

        # get monitors
        monitors = win32api.EnumDisplayMonitors()
        monitors_num = len(monitors)
        window_width = 0
        window_height = 0
        monitor_info = []

        def get_monitor_size(m_width, m_height):
            w_width = abs(m_width) // grid_size[1]
            w_height = m_height // grid_size[0]
            return w_width, w_height

        if monitors_num == 1:
            monitor = monitors[0]
            monitor_info = win32api.GetMonitorInfo(monitor[0])
            _, _, monitor_width, monitor_height = monitor_info["Monitor"]
            window_width, window_height = get_monitor_size(monitor_width, monitor_height)

        elif monitors_num == 2:
            monitor = monitors[1]
            monitor_info = win32api.GetMonitorInfo(monitor[0])
            monitor_width, _, _, monitor_height = monitor_info["Monitor"]
            window_width, window_height = get_monitor_size(monitor_width, monitor_height)

        # align apps
        for j, hwnd in enumerate(windows):
            row = j // grid_size[1]
            col = j % grid_size[1]
            x = monitor_info["Monitor"][0] + col * window_width
            y = monitor_info["Monitor"][1] + row * window_height

            win32gui.MoveWindow(hwnd, x, y, window_width, window_height, True)
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, x, y, window_width + 15, window_height + 7,
                                  win32con.SWP_SHOWWINDOW)
    except Exception as e:
        print(f"Error: {e}")
