# dialog.py
# test
"""Dialog-style application."""

import sys
# import array
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QFormLayout,
    QLineEdit,
    QPushButton,
)


counter = 1
#inputFields = [[mainTextBar, mainButton]]

class Window(QDialog):

    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("QDialog")
        mainButton = QPushButton("+")
        mainTextBar = QLineEdit()
        formLayout = QFormLayout()

        mainTextBar.setObjectName("mainTextBar")

        mainButton.setObjectName("mainButton")
        mainTextBar.setFixedWidth(400)
        mainButton.setFixedWidth(30)
        formLayout.addRow(mainTextBar, mainButton)
        mainButton.clicked.connect(lambda: self._createInputField(formLayout, counter))
        launchButton = QPushButton("Launch all")
        launchButton.show()
        self.setLayout(formLayout)

    def _createInputField(self, formLayout, counter):
        if counter < 19:
            textBar = QLineEdit()
            textBar.setObjectName("textBar" + str(counter))
            textBar.setText(textBar.objectName())
            textBar.setFixedWidth(400)
            button = QPushButton("-")
            button.setFixedWidth(30)
            button.clicked.connect(lambda: self._deleteInputField(textBar, button))
            # inputFields.append([textBar, button])
            formLayout.addRow(textBar, button)
            counter += 1

    def _deleteInputField(self, textBar, button):
        textBar.deleteLater()
        button.deleteLater()


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())
