from ui.login.ui_login import Ui_login_window
from client import db_client


class complete_login_window(Ui_login_window):
    def __init__(self):
        Ui_login_window.__init__(self)
        self.client = db_client()

    def setupUi(self, login_window):
        Ui_login_window.setupUi(self, login_window)
        self.setup_events()

    def setup_events(self):
        self.login_button.clicked.connect(self.login_clicked)
        self.create_account_button.clicked.connect(self.create_account_clicked)

    def login_clicked(self):
        if not self.check_fields():
            return
        self.client.login(self.login_edit.text(), self.password_edit.text())

    def check_fields(self):
        if not self.login_edit.text():
            self.login_edit.setPlaceholderText("you must enter login")
            return False
        if not self.password_edit.text():
            self.password_edit.setPlaceholderText("you must enter password")
            return False
        return True

    def create_account_clicked(self):
        self.login_edit.setText("account")
