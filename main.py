"""Dialog-style application."""
import itertools
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtGui import QIcon
from gui import Window


if __name__ == "__main__":
    try:
        app = QApplication([])
        fontId = QFontDatabase.addApplicationFont("SegoeUI-Light.ttf")
        if fontId < 0:
            print('font not loaded')

        families = QFontDatabase.applicationFontFamilies(fontId)
        if len(families) > 0:
            font = QFont(families[0])

        window = Window()
        icon = QIcon("ico.png")
        window.setWindowIcon(icon)
        window.setGeometry(300, 300, 760, 480)
        window.setFixedSize(760, 480)
        window.show()
        app.exec()
    except Exception as e:
        print(f"Error: {e}")
