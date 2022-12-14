from PyQt6 import QtWidgets
from ui.login.login import login_window
from ui.account_creation.account_creation import account_creation_window
from ui.reader.reader import reader_window
from ui.librarian.librarian import librarian_window
from ui.event_manager.event_manager import event_manager
from ui.speaker.speaker import speaker_window
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
            case window_type.reader:
                self.ui = reader_window(self)
            case window_type.librarian:
                self.ui = librarian_window(self)
            case window_type.event_manager:
                self.ui = event_manager(self)
            case window_type.speaker:
                self.ui = speaker_window(self)
        self.ui.setup()
        self.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ctx = context()
    ctx.change_window(window_type.logging)
    sys.exit(app.exec())
