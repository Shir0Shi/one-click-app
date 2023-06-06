import time

from pywinauto import Application
import psutil


def start_app_processes(widget):
    app_name_a = widget.text()
    try:
        app = Application(backend="uia").start(app_name_a)
        processes_ids.append(app.process)
        processes_names.append(widget)
        print(processes_ids)
    except Exception as e:
        print(f"processes_ids.append 2 Error: {e}")


def close_apps():
    try:

        for a in processes_ids:
            if psutil.pid_exists(a):
                app = Application().connect(process=a)
                wnd = app.top_window().set_focus().send_keystrokes('%{F4}')
                if app.Dialog.exists():  # print_control_identifiers() != None:
                    time.sleep(10)
            else:
                print(f"app with process id {a} was closed")

        processes_ids.clear()
        processes_names.clear()
        mainApp = Application().connect(title="One click app")
        mainApp.top_window().set_focus()
    except Exception as e:
        print(f"close apps func Error: {e}")


processes_ids = []
processes_names = []
