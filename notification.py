from PyQt6.QtWidgets import QMessageBox, QVBoxLayout, QDialog
class NotificationDialog(QDialog):
    def __init__(self, parent=None):
        super(NotificationDialog, self).__init__(parent)
        self.setWindowTitle('Notifications')
        self.layout = QVBoxLayout(self)
        self.setModal(True)

    def add_notification(self, message):
        msg_box = QMessageBox()
        msg_box.setText(message)
        msg_box.addButton(QMessageBox.StandardButton.Ok)
        self.layout.addWidget(msg_box.button(QMessageBox.StandardButton.Ok))
        msg_box.show()
