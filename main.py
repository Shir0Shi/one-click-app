
"""Dialog-style application."""


import itertools
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt, QRect
from pywinauto.application import Application
from pywinauto.keyboard import send_keys
import re
sys._excepthook = sys.excepthook


def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook

textInputWidth = 405
buttonWidth = 30

funButtonWidth = 70
funButtonHeight = 35

prog_amount = 19

processes_ids = []
class Window(QDialog):
    count = 0

    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("One click app")

        scrollBox = QScrollArea(self)
        scrollBox.setGeometry(5, 40, 480, 425)
        scrollBox.setWidgetResizable(True)

        scrollAreaWidgetContents = QWidget()
        scrollAreaWidgetContents.setGeometry(QRect(0, 0, 289, 219))

        formLayout = QFormLayout(scrollAreaWidgetContents)

        mainTextBar = QLineEdit(scrollAreaWidgetContents)

        mainButton = QPushButton(scrollAreaWidgetContents)
        mainTextBar.setObjectName("mainTextBar")
        mainButton.setObjectName("mainButton")
        mainButton.setText("+")
        mainTextBar.setFixedWidth(textInputWidth)
        mainButton.setFixedWidth(buttonWidth)
        formLayout.addRow(mainTextBar, mainButton)
        mainButton.clicked.connect(lambda: self._createInputField(formLayout))

        label = QLabel("Input file paths", self)
        # label.setGeometry(0, 10, 210, 12)
        label.move(0, 0)
        label.setMargin(10)
        label.setFont(QFont("Segoe ui", 15))

        launchButton = QPushButton("Launch all", self)
        launchButton.setGeometry(500, 430, funButtonWidth, funButtonHeight)
        launchButton.show()
        launchButton.clicked.connect(lambda: self.launchApps())

        closeButton = QPushButton("Close all", self)
        closeButton.setGeometry(590, 430, funButtonWidth, funButtonHeight)
        closeButton.show()
        closeButton.clicked.connect(lambda: self.closeApps())

        saveButton = QPushButton("Save set", self)
        saveButton.setGeometry(680, 430, funButtonWidth, funButtonHeight)
        saveButton.show()

        # createMainField(scrollBox)
        scrollBox.setWidget(scrollAreaWidgetContents)
        label.show()
        # scrollBox.setLayout(formLayout)
        # scrollBox.show()

        # self.setLayout(formLayout)

    def _createInputField(self, formLayout):
        if self.count < prog_amount:
            self.count += 1  # newId = next(iter(self.count))
            textBar = QLineEdit()
            button = QPushButton("-")
            textBar.setObjectName("textBar" + str(self.count))  # self.newId
            # textBar.setText(str(self.count))
            textBar.setFixedWidth(textInputWidth)
            button.setFixedWidth(buttonWidth)
            button.clicked.connect(lambda: self._deleteInputField(textBar, button))
            formLayout.addRow(textBar, button)

    def _deleteInputField(self, textBar, button):
        if int(re.findall(r'\d+', textBar.objectName())[0]) < self.count:
            widget_a = self.findChild(QLineEdit, "textBar" + str(self.count))
            temp_name = textBar.objectName()
            textBar.deleteLater()
            button.deleteLater()
            widget_a.setObjectName(temp_name)
            # widget_a.setText(temp_name)
            self.count -= 1
        else:
            textBar.deleteLater()
            button.deleteLater()
            self.count -= 1

    # app.window(title_re=".*Part of Title.*")

    def launchApps(self):
        widget = self.findChild(QLineEdit, "mainTextBar")

        app_name = widget.text()
        try:
            main_app = Application(backend="uia").start(app_name)
            processes_ids.append(main_app.process)
        except:
            print("ERROR")
            print(sys.excepthook)
        for i in range(1, self.count+1):
            widget_a = self.findChild(QLineEdit, "textBar" + str(i))
            if widget_a:
                app_name_a = widget_a.text()
                print(app_name_a)
                try:
                    app = Application(backend="uia").start(app_name_a)
                    processes_ids.append(app.process)
                    print(processes_ids)
                except:
                    print("ERROR")
                    print(sys.excepthook)

        print(app_name)
# TODO: closeButton function
    def closeApps(self):
        for a in processes_ids:
            app = Application().connect(process=a)
            wnd = app.top_window()
            wnd.send_chars('aaa')
            #app.window(title=wnd.texts()[0]).send_keystrokes('%{F4}')


if __name__ == "__main__":
    app = QApplication([])
    fontId = QFontDatabase.addApplicationFont("SegoeUI-Light.ttf")
    if fontId < 0:
        print('font not loaded')

    families = QFontDatabase.applicationFontFamilies(fontId)
    if len(families) > 0:
        font = QFont(families[0])

    window = Window()
    window.setGeometry(300, 300, 760, 480)
    window.show()
    try:
        sys.exit(app.exec())
    except:
        print("Exiting")
