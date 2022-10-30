<<<<<<< HEAD
=======
# dialog.py
# test
"""Dialog-style application."""
>>>>>>> 0a9c1628f84cc0e1c5c9edbe25129c77c910e075

import itertools
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt, QRect

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

        closeButton = QPushButton("Close all", self)
        closeButton.setGeometry(590, 430, funButtonWidth, funButtonHeight)
        closeButton.show()

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
        self.count += 1  # newId = next(iter(self.count))
        textBar = QLineEdit()
        button = QPushButton("-")
        textBar.setObjectName("textBar" + str(self.count))  # self.newId
        textBar.setFixedWidth(textInputWidth)
        button.setFixedWidth(buttonWidth)
        button.clicked.connect(lambda: self._deleteInputField(textBar, button))
        if self.count < 20:
            formLayout.addRow(textBar, button)

    def _deleteInputField(self, textBar, button):
        textBar.deleteLater()
        button.deleteLater()


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
