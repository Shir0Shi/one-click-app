
"""Dialog-style application."""


import itertools
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt, QRect
from pywinauto.application import Application
from pywinauto.keyboard import send_keys
import re
import time
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
buttonWidth = 25

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


        mainButton = QPushButton(scrollAreaWidgetContents) # scrollAreaWidgetContents
        mainTextBar.setObjectName("mainTextBar")
        mainButton.setObjectName("mainButton")
        mainButton.setText("+")

        fileButton = QPushButton(scrollAreaWidgetContents)
        fileButton.setObjectName("fileButton")
        fileButton.setText("file")
        fileButton.setFixedWidth(25)
        fileButton.clicked.connect(lambda: self._openDirectory(mainTextBar))

        mainTextBar.setFixedWidth(textInputWidth)
        mainButton.setFixedWidth(buttonWidth)
        formLayout.addRow(mainTextBar, fileButton)
        mainButton.clicked.connect(lambda: self._createInputField(formLayout))

        mainButton.show()
        mainButton.setGeometry(450, 8, 25, 25)
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

    #filepath = QFileDialog.getOpenFileName(self, 'Hey! Select a File')
    #    filepath.show()
    def _openDirectory(self, line):
        #dialog = QFileDialog()
        # try:
        self.getOpenFilesAndDirs()
            # foo_dir = QFileDialog.getOpenFileName(
            #     parent=self,
            #     caption='Select file',
            #     directory='C:\\',
            #     filter='*.exe',)
            # print(foo_dir)
        # except:
        #     print("wtf")
        #dialog = QFileDialog()
        #dialog = QFileDialog(self)
        #dialog.setFileMode(QFileDialog.directoryUrl)
        #dialog.setSidebarUrls([QUrl.fromLocalFile()])
        # if dialog.exec() == QDialog.Accepted:
        #     self._audio_file = dialog.selectedFiles()[0]
        #folder_path = dialog.getExistingDirectory(None, "Select Folder")
        #folderpath = QFileDialog.getExistingDirectory(self, 'Select Folder')
        # fname= QFileDialog.getOpenFileName(self, 'Open file', '', '', options=QFileDialog.DontUseNativeDialog)
        #filepath = str(dialog.getOpenFileName(self, 'Open file', '', ''))
        #line.txt(filepath)
        #filepath.show()
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
# TODO: fix bug with detecting saveWindow
    def closeApps(self):
        try:
            for a in processes_ids:
                app = Application().connect(process=a)
                #app

                wnd = app.top_window().set_focus().send_keystrokes('%{F4}')
                if app.Dialog.exists(): # print_control_identifiers() != None:
                    time.sleep(10)
            # for x in app.descendants():
            #     print(x.window_text())
            #     print(x.class_name())
            #print(wnd.texts()[0])
            #if app.popup_window():
            #
            processes_ids.clear()
            mainApp = Application().connect(title="One click app")
            mainApp.top_window().set_focus()
        except:
            print("ERROR")
            print(sys.excepthook)

            # window().set_focus()
            # wnd.send_chars('aaa')
            #app.window(title=wnd.texts()[0])
            # notepad.exe

    def getOpenFilesAndDirs(parent=None, caption='', directory='D:\\',
                            filter='*.exe', initialFilter='', options=None):
        #def updateText():
        #    # update the contents of the line edit widget with the selected files
        #    selected = []
        #    for index in view.selectionModel().selectedRows():
        #        selected.append('"{}"'.format(index.data()))
        #    lineEdit.setText(' '.join(selected))

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
        # by default, if a directory is opened in file listing mode,
        # QFileDialog.accept() shows the contents of that directory, but we
        # need to be able to "open" directories as we can do with files, so we
        # just override accept() with the default QDialog implementation which
        # will just return exec_()
        dialog.accept = lambda: QDialog.accept(dialog)

        # there are many item views in a non-native dialog, but the ones displaying
        # the actual contents are created inside a QStackedWidget; they are a
        # QTreeView and a QListView, and the tree is only used when the
        # viewMode is set to QFileDialog.Details, which is not this case
        stackedWidget = dialog.findChild(QStackedWidget)
        view = stackedWidget.findChild(QListView)
        #view.selectionModel().selectionChanged.connect(updateText)

        lineEdit = dialog.findChild(QLineEdit)
        # clear the line edit contents whenever the current directory changes
        dialog.directoryEntered.connect(lambda: lineEdit.setText(''))

        dialog.exec()
        print(dialog.selectedFiles())

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
