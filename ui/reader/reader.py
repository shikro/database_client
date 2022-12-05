from ui.reader.ui_reader import Ui_reader_window


class reader_window(Ui_reader_window):
    def __init__(self, context):
        super().__init__()
        self.context = context

    def setup(self):
        Ui_reader_window.setupUi(self, self.context)
        self._setup_account_info_fields()
        self._setup_events()

    def _setup_account_info_fields(self):
        self.name_edit.setText(self.context.db_client.name)
        self.phone_edit.setText(self.context.db_client.phone)
        self.email_edit.setText(self.context.db_client.email)
        self.password_edit.setText(self.context.db_client.password)

    def _setup_events(self):
        self.update_info_button.clicked.connect(self._update_info_clicked)

    def _update_info_clicked(self):
        if not self._check_account_info_fields():
            return
        self.context.db_client.update_account_info(new_name=self.name_edit.text(),
                                                   new_email=self.email_edit.text(),
                                                   new_password=self.password_edit.text())

    def _check_account_info_fields(self):
        placeholder_text = "can't be empty"
        res = True
        if not self.name_edit.text():
            self.name_edit.setPlaceholderText(placeholder_text)
            res = False
        if not self.password_edit.text():
            self.password_edit.setPlaceholderText(placeholder_text)
            res = False
        return res
