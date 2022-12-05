from ui.login.ui_login import Ui_login_window
from ui.window_types import window_type


class login_window(Ui_login_window):
    def __init__(self, context):
        super().__init__()
        self.context = context

    def setup(self):
        Ui_login_window.setupUi(self, self.context)
        self._setup_events()

    def _setup_events(self):
        self.login_button.clicked.connect(self._login_clicked)
        self.create_account_button.clicked.connect(self._create_account_clicked)

    def _login_clicked(self):
        if not self._check_fields():
            return
        error_msg = self.context.db_client.login(self.login_edit.text(), self.password_edit.text())
        if error_msg:
            self.error_label.setText(error_msg)
        else:
            self.context.change_window(window_type.main)

    def _check_fields(self):
        res = True
        if not self.login_edit.text():
            self.login_edit.setPlaceholderText("you must enter login")
            res = False
        if not self.password_edit.text():
            self.password_edit.setPlaceholderText("you must enter password")
            res = False
        return res

    def _create_account_clicked(self):
        self.context.change_window(window_type.account_creation)
