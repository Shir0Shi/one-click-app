from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt, QRect, QPoint
from pywinauto.application import Application
from pywinauto.keyboard import send_keys
from pywinauto import Desktop, win32functions
import re
import time
import os.path
import json
import uuid
import psutil
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import QApplication, QWidget
import math
import pywinauto
import win32api
import win32con
import win32gui
import win32process
from notification import NotificationDialog

desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

TEXT_INPUT_WIDTH = 405
BUTTON_WIDTH = 25

FUN_BUTTON_WIDTH = 70
FUN_BUTTON_HEIGHT = 35

PROG_AMOUNT = 19

SET_BUTTONS_POS_X = 500
SET_BUTTONS_POS_Y = 240

ALIGN_BUTTONS_POS_X = 500
ALIGN_BUTTONS_POS_Y = 300

ALIGN_BUTTON_WIDTH = 90
ALIGN_BUTTON_HEIGHT = 35

processes_ids = []
processes_names = []

windows = []

sets_file = "sets.json"


class Window(QMainWindow):
    data = {}
    set_name = ""
    inputFields = []
    decreaseFieldButtons = []
    fileButtons = []
    setIsOpen = False
    lastOpenSetId = ""

    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("One click app")

        #########################################################
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setGeometry(SET_BUTTONS_POS_X, 40, 240, 180)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_widget.setGeometry(QRect(SET_BUTTONS_POS_X, 0, 289, 219))
        self.scroll_area.setWidget(self.scroll_widget)

        self.load_sets()
        ###########################################################

        scrollBox = QScrollArea(self)
        scrollBox.setGeometry(5, 40, 480, 425)
        scrollBox.setWidgetResizable(True)

        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 289, 219))

        self.formLayout = QFormLayout(self.scrollAreaWidgetContents)
        self.mainTextBar = QLineEdit(self.scrollAreaWidgetContents)

        mainButton = QPushButton(self.scrollAreaWidgetContents)  # scrollAreaWidgetContents
        self.mainTextBar.setObjectName("mainTextBar")
        mainButton.setObjectName("mainButton")
        mainButton.setText("+")

        fileButton = QPushButton(self.scrollAreaWidgetContents)
        fileButton.setObjectName("fileButton")
        fileButton.setText("file")
        fileButton.setFixedWidth(25)
        fileButton.clicked.connect(lambda: self.getOpenFilesAndDirs(editLine=self.mainTextBar))

        self.mainTextBar.setFixedWidth(TEXT_INPUT_WIDTH)
        mainButton.setFixedWidth(BUTTON_WIDTH)
        self.formLayout.addRow(self.mainTextBar, fileButton)
        mainButton.clicked.connect(lambda: self._createInputField())

        mainButton.show()
        mainButton.setGeometry(450, 8, 25, 25)

        label = QLabel("Input file paths", self)
        label.setGeometry(0, 0, 210, 40)
        # label.move(0, 0)
        label.setMargin(10)
        label.setFont(QFont("Segoe ui", 15))

        self.setName = QLineEdit(self)
        self.setName.setFixedWidth(150)
        self.setName.setFixedHeight(20)
        self.setName.move(scrollBox.width() - self.setName.width() + 5, 10)
        # self.setName.setDisabled(True)
        self.update_input_field(self.set_name)

        launchButton = QPushButton("Launch all", self)
        launchButton.setGeometry(500, 430, FUN_BUTTON_WIDTH, FUN_BUTTON_HEIGHT)
        launchButton.show()
        launchButton.clicked.connect(lambda: self.launchApps())

        closeButton = QPushButton("Close all", self)
        closeButton.setGeometry(580, 430, FUN_BUTTON_WIDTH, FUN_BUTTON_HEIGHT)
        closeButton.show()
        closeButton.clicked.connect(lambda: self.closeApps())

        newSetButton = QPushButton("New set", self)
        newSetButton.setGeometry(SET_BUTTONS_POS_X, SET_BUTTONS_POS_Y, FUN_BUTTON_WIDTH, FUN_BUTTON_HEIGHT)
        newSetButton.show()
        newSetButton.clicked.connect(lambda: self.createNewSet())

        saveButton = QPushButton("Save set", self)
        saveButton.setGeometry(SET_BUTTONS_POS_X + FUN_BUTTON_WIDTH + 15, SET_BUTTONS_POS_Y, FUN_BUTTON_WIDTH,
                               FUN_BUTTON_HEIGHT)
        saveButton.show()
        saveButton.clicked.connect(lambda: self.saveSet())

        self.deleteButton = QPushButton("Delete set", self)
        self.deleteButton.setGeometry(SET_BUTTONS_POS_X + (FUN_BUTTON_WIDTH + 15) * 2, SET_BUTTONS_POS_Y,
                                      FUN_BUTTON_WIDTH, FUN_BUTTON_HEIGHT)
        self.deleteButton.show()
        self.deleteButton.clicked.connect(lambda: self.deleteSet())
        self.deleteButton.setDisabled(True)

        self.alignButton = QPushButton("Align screens", self)
        self.alignButton.setGeometry(ALIGN_BUTTONS_POS_X, ALIGN_BUTTONS_POS_Y, ALIGN_BUTTON_WIDTH, ALIGN_BUTTON_HEIGHT)
        self.alignButton.show()
        self.alignButton.clicked.connect(lambda: self.align_windows())

        self.createBatButton = QPushButton("Create .bat", self)
        self.createBatButton.setGeometry(ALIGN_BUTTONS_POS_X+ALIGN_BUTTON_WIDTH+60, ALIGN_BUTTONS_POS_Y, ALIGN_BUTTON_WIDTH, ALIGN_BUTTON_HEIGHT)
        self.createBatButton.show()
        self.createBatButton.clicked.connect(lambda: self.create_bat())
        self.createBatButton.setDisabled(True)

        scrollBox.setWidget(self.scrollAreaWidgetContents)

        label.show()

    def create_bat(self):
        self.createBatButton.setDisabled(True)
        # if self.setIsOpen and self.lastOpenSetId != "":
        #     try:
        #         app_list = []
        #
        #         for i, set_ in enumerate(self.data):
        #             if set_["id"] == self.lastOpenSetId:
        #                 app_list = set_["fields_to_load"]
        #         filename = os.path.join(desktop_path, self.setName.text())
        #         with open(filename, 'w') as f:
        #             for app in app_list:
        #                 f.write('start "" "{}"\n'.format(app))
        #     except Exception as e:
        #         print(f"Error: {e}")

    def rewriteSetFile(self, set_data=[]):
        with open(sets_file, "w") as f:
            json.dump(set_data, f, indent=4)

    def load_sets(self):

        if not os.path.exists(sets_file):
            self.rewriteSetFile()
        try:
            with open(sets_file, "r") as f:
                self.data = json.load(f)
            if self.data:
                for set_data in self.data:
                    set_name = set_data["name"]
                    set_id = set_data["id"]
                    set_button = QPushButton(set_name, self.scroll_widget)
                    set_button.clicked.connect(lambda state, id=set_id: self.on_set_button_clicked(id))
                    self.scroll_layout.addWidget(set_button)
            else:
                print("No sets found in sets.json")
        except Exception as e:
            print(f"Error: {e}")

    def reload_sets(self):
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                self.scroll_layout.removeItem(item)
        self.load_sets()

    def get_windows(self):
        win_info = []
        excluded_apps = ['Microsoft Text Input Application', 'Параметры', 'Settings', 'One click app']

        def isRealWindow(hWnd):
            '''Return True iff given window is a real Windows application window.'''
            if not win32gui.IsWindowVisible(hWnd):
                return False
            if win32gui.GetParent(hWnd) != 0:
                return False
            if win32gui.IsIconic(hWnd):
                return False
            hasNoOwner = win32gui.GetWindow(hWnd, win32con.GW_OWNER) == 0
            lExStyle = win32gui.GetWindowLong(hWnd, win32con.GWL_EXSTYLE)
            if (((lExStyle & win32con.WS_EX_TOOLWINDOW) == 0 and hasNoOwner)
                    or ((lExStyle & win32con.WS_EX_APPWINDOW != 0) and not hasNoOwner)):
                window_text = win32gui.GetWindowText(hWnd)
                if window_text:
                    return True
            return False

        def callback(hWnd, windows):
            if not isRealWindow(hWnd):
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

    def align_windows(self):
        try:
            # получаем список окон
            windows, win_info = self.get_windows()
            print(windows)
            print(win_info)
            num_windows = len(windows)

            if num_windows == 0:
                print("No running applications found")
                return

            # Определяем тип сетки в зависимости от количества окон
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

            for j, hwnd in enumerate(windows):
                row = j // grid_size[1]
                col = j % grid_size[1]
                x = monitor_info["Monitor"][0] + col * window_width
                y = monitor_info["Monitor"][1] + row * window_height

                win32gui.MoveWindow(hwnd, x, y, window_width, window_height, True)
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, x, y, window_width+15, window_height+7,
                                      win32con.SWP_SHOWWINDOW)
        except Exception as e:
            print(f"Error: {e}")

    def on_set_button_clicked(self, set_id):
        try:
            self.deleteAllFields()
            self.deleteButton.setDisabled(False)
            self.createBatButton.setDisabled(False)
            for set_data in self.data:
                if set_data["id"] == set_id:
                    self.setIsOpen = True
                    self.lastOpenSetId = set_data["id"]
                    self.update_input_field(set_data["name"])
                    self.mainTextBar.setText(set_data["fields_to_load"][0])
                    for field in set_data["fields_to_load"][1:]:
                        self._createInputField(field)
                    break
        except Exception as e:
            print(f"Error: {e}")

    def createNewSet(self):
        self.deleteButton.setDisabled(True)
        self.createBatButton.setDisabled(True)
        self.update_input_field("")
        self.deleteAllFields()
        self.mainTextBar.setText("")
        self.setIsOpen = False
        self.lastOpenSetId = ""
        # self.setName.setDisabled(False)

    def update_input_field(self, set_name):
        self.setName.setText(set_name)

    def saveSet(self):
        try:
            set_name = self.setName.text()
            set_id = str(uuid.uuid4())
            if self.setIsOpen and self.lastOpenSetId != "":
                set_id = self.lastOpenSetId

            # for set_data in self.data:
            #     if set_data["name"] == set_name:
            #         set_name = set_name + "copy"

            if set_name == "":
                notification_dialog = NotificationDialog()
                notification_dialog.add_notification("First click 'New set' and than input some set name")
                notification_dialog.show()
                return

            fields_to_load = self.getFields()
            new_set = {
                "id": set_id,
                "name": set_name,
                "fields_to_load": fields_to_load
            }
            self.updateSetData(new_set)
            self.rewriteSetFile(self.data)

            self.reload_sets()

        except Exception as e:
            print(f"Delete fields Error: {e}")

    def updateSetData(self, new_set):
        for i, set_ in enumerate(self.data):
            if set_["id"] == new_set["id"]:
                self.data[i] = new_set
                return
        self.data.append(new_set)

    def getFields(self):
        fields_to_load = []
        fields_to_load.append(self.mainTextBar.text())
        for prog in self.inputFields:
            if prog.text() != "":
                fields_to_load.append(prog.text())
        return fields_to_load

    def deleteSet(self):
        self.deleteButton.setDisabled(True)
        self.createBatButton.setDisabled(True)
        if self.setIsOpen and self.lastOpenSetId != "":
            for i, set_ in enumerate(self.data):
                if set_["id"] == self.lastOpenSetId:
                    self.data.pop(i)
                    break
            self.rewriteSetFile(self.data)
            self.reload_sets()
        print("Delete set")

    def _createInputField(self, textBarText=""):
        if len(self.inputFields) < PROG_AMOUNT:

            textBar = QLineEdit(textBarText)
            openFileButton = QPushButton("file")
            openFileButton.setFixedWidth(25)
            decreaseButton = QPushButton(self.scrollAreaWidgetContents)
            decreaseButton.setText("-")

            textBar.setFixedWidth(TEXT_INPUT_WIDTH)

            openFileButton.clicked.connect(lambda: self.getOpenFilesAndDirs(editLine=textBar))

            self.formLayout.addRow(textBar, openFileButton)

            decreaseButton.setGeometry(450, ((len(self.inputFields) + 1) * 30) + 7, 25, 25)

            decreaseButton.show()

            self.inputFields.append(textBar)
            self.decreaseFieldButtons.append(decreaseButton)
            self.fileButtons.append(openFileButton)
            try:
                index = self.inputFields.index(textBar)
                decreaseButton.clicked.connect(lambda: self._deleteInputField(index))
            except ValueError:
                print("Some error occur ")

    def _deleteInputField(self, pos):
        try:
            if self.inputFields[pos] in processes_names:
                index = processes_names.index(self.inputFields[pos])
                processes_names.pop(index)
                processes_ids.pop(index)
            print(pos)
            self.inputFields[pos].deleteLater()
            self.inputFields.pop(pos)
            self.decreaseFieldButtons[pos].deleteLater()
            self.decreaseFieldButtons.pop(pos)
            self.fileButtons[pos].deleteLater()
            self.fileButtons.pop(pos)
            self.redrawButtons()
        except Exception as e:
            print(f"Delete fields Error: {e}")

    def deleteAllFields(self):
        for i in range(len(self.inputFields)):
            self.inputFields[i].deleteLater()
            self.decreaseFieldButtons[i].deleteLater()
            self.fileButtons[i].deleteLater()
        self.inputFields = []
        self.decreaseFieldButtons = []
        self.fileButtons = []

    def redrawButtons(self):
        for i, button in enumerate(self.decreaseFieldButtons):
            button.setGeometry(450, (i + 1) * 30 + 7, 25, 25)

    def launchApps(self):
        widget_main = self.findChild(QLineEdit, "mainTextBar")
        if len(processes_ids) < len(self.inputFields):
            print(f"{len(processes_ids)} < {len(self.inputFields)}")
            app_name = widget_main.text()
            try:
                main_app = Application(backend="uia").start(app_name)
                processes_ids.append(main_app.process)
                processes_names.append(widget_main)
            except Exception as e:
                print(f"processes_ids.append 1 Error: {e}")
            for widget in self.inputFields:
                app_name_a = widget.text()
                print(app_name_a)
                try:
                    app = Application(backend="uia").start(app_name_a)
                    processes_ids.append(app.process)
                    processes_names.append(widget)
                    print(processes_ids)
                except Exception as e:
                    print(f"processes_ids.append 2 Error: {e}")
        else:
            print(f"{len(processes_ids)} > or == {len(self.inputFields)}")
            for widget in self.inputFields:
                if widget not in processes_names:
                    app_name_a = widget.text()
                    print(app_name_a)
                    try:
                        app = Application(backend="uia").start(app_name_a)
                        processes_ids.append(app.process)
                        processes_names.append(widget)
                        print(processes_ids)
                    except Exception as e:
                        print(f"processes_ids.append 3 Error: {e}")

    def closeApps(self):
        try:
            for a in processes_ids:
                app = Application().connect(process=a)
                wnd = app.top_window().set_focus().send_keystrokes('%{F4}')
                if app.Dialog.exists():  # print_control_identifiers() != None:
                    time.sleep(10)
            processes_ids.clear()
            processes_names.clear()
            mainApp = Application().connect(title="One click app")
            mainApp.top_window().set_focus()
        except Exception as e:
            print(f"close apps func (173-182) Error: {e}")

    def getOpenFilesAndDirs(parent=None,
                            caption='',
                            directory='D:\\',
                            filter='*.exe',
                            initialFilter='',
                            options=None,
                            editLine=QLineEdit
                            ):
        dialog = QFileDialog(parent, windowTitle=caption)
        dialog.setFileMode(dialog.FileMode.ExistingFiles)
        if options:
            dialog.setOptions(options)
        dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
        if directory:
            dialog.setDirectory(directory)
        if filter:
            dialog.setNameFilter(filter)
            if initialFilter:
                dialog.selectNameFilter(initialFilter)
        dialog.accept = lambda: QDialog.accept(dialog)
        stackedWidget = dialog.findChild(QStackedWidget)
        view = stackedWidget.findChild(QListView)
        # view.selectionModel().selectionChanged.connect(updateText)
        lineEdit = dialog.findChild(QLineEdit)
        dialog.directoryEntered.connect(lambda: lineEdit.setText(''))
        dialog.exec()
        if dialog.selectedFiles():
            editLine.setText(dialog.selectedFiles()[0])
