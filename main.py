from PyQt6 import QtWidgets
from ui.login.login import login_window
from ui.account_creation.account_creation import account_creation_window
from ui.window_types import window_type
from client import db_client

import sys


class context(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = None
        self.db_client = db_client()

    def change_window(self, window):
        self.hide()
        match window:
            case window_type.logging:
                self.ui = login_window(self)
            case window_type.account_creation:
                self.ui = account_creation_window(self)
            case window_type.main:
                print("main")
        self.ui.setup()
        self.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ctx = context()
    ctx.change_window(window_type.logging)
    sys.exit(app.exec())
