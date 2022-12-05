from ui.account_creation.ui_account_creation import Ui_account_creation_window
from ui.window_types import window_type


class account_creation_window(Ui_account_creation_window):
    def __init__(self, context):
        super().__init__()
        self.context = context

    def setup(self):
        Ui_account_creation_window.setupUi(self, self.context)
        self._setup_events()

    def _setup_events(self):
        self.create_button.clicked.connect(self._create_clicked)
        self.cancel_button.clicked.connect(self._cancel_clicked)

    def _create_clicked(self):
        if not self._check_fields():
            return
        # TODO account creation

    def _check_fields(self):
        res = True
        if not self.name_edit.text():
            self.name_edit.setPlaceholderText("enter name")
            res = False
        if not self.phone_edit.text():
            self.phone_edit.setPlaceholderText("enter phone number")
            res = False
        if not self.password_edit.text():
            self.password_edit.setPlaceholderText("enter password")
            res = False
        return res


    def _cancel_clicked(self):
        self.context.change_window(window_type.logging)
