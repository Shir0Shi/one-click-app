import os.path
import uuid

from PyQt6.QtCore import QRect
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QWidget
from pywinauto.application import Application

from notification import NotificationDialog
from running_app_functions import start_app_processes, close_apps, processes_ids, processes_names
from set_file_functions import rewrite_set_file, load_data, update_set_data
from windows_functions import align_windows

import psutil

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


class Window(QMainWindow):

    set_name = ""
    inputFields = []
    decreaseFieldButtons = []
    fileButtons = []
    setIsOpen = False
    lastOpenSetId = ""
    data = load_data()

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
        fileButton.clicked.connect(lambda: self.get_open_files_and_dirs(edit_line=self.mainTextBar))

        self.mainTextBar.setFixedWidth(TEXT_INPUT_WIDTH)
        mainButton.setFixedWidth(BUTTON_WIDTH)
        self.formLayout.addRow(self.mainTextBar, fileButton)
        mainButton.clicked.connect(lambda: self._create_input_field())

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
        launchButton.clicked.connect(lambda: self.launch_apps())

        closeButton = QPushButton("Close all", self)
        closeButton.setGeometry(580, 430, FUN_BUTTON_WIDTH, FUN_BUTTON_HEIGHT)
        closeButton.show()
        closeButton.clicked.connect(lambda: close_apps())

        newSetButton = QPushButton("New set", self)
        newSetButton.setGeometry(SET_BUTTONS_POS_X, SET_BUTTONS_POS_Y, FUN_BUTTON_WIDTH, FUN_BUTTON_HEIGHT)
        newSetButton.show()
        newSetButton.clicked.connect(lambda: self.create_new_set())

        saveButton = QPushButton("Save set", self)
        saveButton.setGeometry(SET_BUTTONS_POS_X + FUN_BUTTON_WIDTH + 15, SET_BUTTONS_POS_Y, FUN_BUTTON_WIDTH,
                               FUN_BUTTON_HEIGHT)
        saveButton.show()
        saveButton.clicked.connect(lambda: self.save_set())

        self.deleteButton = QPushButton("Delete set", self)
        self.deleteButton.setGeometry(SET_BUTTONS_POS_X + (FUN_BUTTON_WIDTH + 15) * 2, SET_BUTTONS_POS_Y,
                                      FUN_BUTTON_WIDTH, FUN_BUTTON_HEIGHT)
        self.deleteButton.show()
        self.deleteButton.clicked.connect(lambda: self.delete_set())
        self.deleteButton.setDisabled(True)

        self.alignButton = QPushButton("Align screens", self)
        self.alignButton.setGeometry(ALIGN_BUTTONS_POS_X, ALIGN_BUTTONS_POS_Y, ALIGN_BUTTON_WIDTH, ALIGN_BUTTON_HEIGHT)
        self.alignButton.show()
        self.alignButton.clicked.connect(lambda: align_windows())

        self.createBatButton = QPushButton("Create .bat", self)
        self.createBatButton.setGeometry(ALIGN_BUTTONS_POS_X + ALIGN_BUTTON_WIDTH + 60, ALIGN_BUTTONS_POS_Y,
                                         ALIGN_BUTTON_WIDTH, ALIGN_BUTTON_HEIGHT)
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
        #         for i, set_ in enumerate(data):
        #             if set_["id"] == self.lastOpenSetId:
        #                 app_list = set_["fields_to_load"]
        #         filename = os.path.join(desktop_path, self.setName.text())
        #         with open(filename, 'w') as f:
        #             for app in app_list:
        #                 f.write('start "" "{}"\n'.format(app))
        #     except Exception as e:
        #         print(f"Error: {e}")

    def load_sets(self):
        try:
            if self.data:
                for set_data in self.data:
                    set_name = set_data["name"]
                    set_id = set_data["id"]
                    set_button = QPushButton(set_name, self.scroll_widget)
                    set_button.clicked.connect(lambda state, button_id=set_id: self.on_set_button_clicked(button_id))
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

    def on_set_button_clicked(self, set_id):
        try:
            self.delete_all_fields()
            self.deleteButton.setDisabled(False)
            self.createBatButton.setDisabled(False)
            for set_data in self.data:
                if set_data["id"] == set_id:
                    self.setIsOpen = True
                    self.lastOpenSetId = set_data["id"]
                    self.update_input_field(set_data["name"])
                    self.mainTextBar.setText(set_data["fields_to_load"][0])
                    for field in set_data["fields_to_load"][1:]:
                        self._create_input_field(field)
                    break
        except Exception as e:
            print(f"Error: {e}")

    def create_new_set(self):
        self.deleteButton.setDisabled(True)
        self.createBatButton.setDisabled(True)
        self.update_input_field("")
        self.delete_all_fields()
        self.mainTextBar.setText("")
        self.setIsOpen = False
        self.lastOpenSetId = ""
        # self.setName.setDisabled(False)

    def update_input_field(self, set_name):
        self.setName.setText(set_name)

    def save_set(self):
        try:
            set_name = self.setName.text()
            set_id = str(uuid.uuid4())
            if self.setIsOpen and self.lastOpenSetId != "":
                set_id = self.lastOpenSetId

            # for set_data in data:
            #     if set_data["name"] == set_name:
            #         set_name = set_name + "copy"

            if set_name == "":
                notification_dialog = NotificationDialog()
                notification_dialog.add_notification("First click 'New set' and than input some set name")
                notification_dialog.show()
                return

            fields_to_load = self.get_fields()
            new_set = {
                "id": set_id,
                "name": set_name,
                "fields_to_load": fields_to_load
            }
            self.data = update_set_data(new_set, self.data)
            rewrite_set_file(self.data)
            self.reload_sets()

        except Exception as e:
            print(f"Delete fields Error: {e}")

    def get_fields(self):
        fields_to_load = []
        fields_to_load.append(self.mainTextBar.text())
        for prog in self.inputFields:
            if prog.text() != "":
                fields_to_load.append(prog.text())
        return fields_to_load

    def delete_set(self):
        self.deleteButton.setDisabled(True)
        self.createBatButton.setDisabled(True)
        if self.setIsOpen and self.lastOpenSetId != "":
            for i, set_ in enumerate(self.data):
                if set_["id"] == self.lastOpenSetId:
                    self.data.pop(i)
                    break
            rewrite_set_file(self.data)
            self.reload_sets()
        print("Delete set")

    def _create_input_field(self, text_bar_text=""):
        if len(self.inputFields) < PROG_AMOUNT:

            textBar = QLineEdit(text_bar_text)
            openFileButton = QPushButton("file")
            openFileButton.setFixedWidth(25)
            decreaseButton = QPushButton(self.scrollAreaWidgetContents)
            decreaseButton.setText("-")

            textBar.setFixedWidth(TEXT_INPUT_WIDTH)
            openFileButton.clicked.connect(lambda: self.get_open_files_and_dirs(edit_line=textBar))
            self.formLayout.addRow(textBar, openFileButton)
            decreaseButton.setGeometry(450, ((len(self.inputFields) + 1) * 30) + 7, 25, 25)
            decreaseButton.show()

            self.inputFields.append(textBar)
            self.decreaseFieldButtons.append(decreaseButton)
            self.fileButtons.append(openFileButton)
            try:
                index = self.inputFields.index(textBar)
                decreaseButton.clicked.connect(lambda: self._delete_input_field(index))
            except ValueError:
                print("Some error occur ")

    def _delete_input_field(self, pos):
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
            self.redraw_buttons()
        except Exception as e:
            print(f"Delete fields Error: {e}")

    def delete_all_fields(self):
        for i in range(len(self.inputFields)):
            self.inputFields[i].deleteLater()
            self.decreaseFieldButtons[i].deleteLater()
            self.fileButtons[i].deleteLater()
        self.inputFields = []
        self.decreaseFieldButtons = []
        self.fileButtons = []

    def redraw_buttons(self):
        for i, button in enumerate(self.decreaseFieldButtons):
            button.setGeometry(450, (i + 1) * 30 + 7, 25, 25)

    def launch_apps(self):
        widget_main = self.findChild(QLineEdit, "mainTextBar")
        indexes = []
        for a in processes_ids:
            if not psutil.pid_exists(a):
                indexes.append(processes_ids.index(a))
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
                start_app_processes(widget)
        elif len(indexes) > 0:
            print(f"processes_ids = {len(processes_ids)} inputFields = {len(self.inputFields)} perhaps {len(indexes)} app was closed")
            for a in indexes:
                Application(backend="uia").start(processes_names[a].text())
        else:
            print(f"{len(processes_ids)} > or == {len(self.inputFields)}")
            for widget in self.inputFields:
                if widget not in processes_names:
                    start_app_processes(widget)

    def get_open_files_and_dirs(self,
                                caption='',
                                directory='D:\\',
                                file_filter='*.exe',
                                initial_filter='',
                                options=None,
                                edit_line=QLineEdit
                                ):
        dialog = QFileDialog(self, windowTitle=caption)
        dialog.setFileMode(dialog.FileMode.ExistingFiles)
        if options:
            dialog.setOptions(options)
        dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
        if directory:
            dialog.setDirectory(directory)
        if file_filter:
            dialog.setNameFilter(file_filter)
            if initial_filter:
                dialog.selectNameFilter(initial_filter)
        dialog.accept = lambda: QDialog.accept(dialog)
        stackedWidget = dialog.findChild(QStackedWidget)
        view = stackedWidget.findChild(QListView)
        # view.selectionModel().selectionChanged.connect(updateText)
        lineEdit = dialog.findChild(QLineEdit)
        dialog.directoryEntered.connect(lambda: lineEdit.setText(''))
        dialog.exec()
        if dialog.selectedFiles():
            edit_line.setText(dialog.selectedFiles()[0])


