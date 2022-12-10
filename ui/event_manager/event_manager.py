from ui.event_manager.ui_event_manager import Ui_event_manager_window
from PyQt6 import QtWidgets, QtCore
import datetime


def create_item(text):
    item = QtWidgets.QTableWidgetItem(text)
    item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
    return item


class speaker_checkbox(QtWidgets.QCheckBox):
    def __init__(self, parent, speaker_id):
        super().__init__(parent)
        self.speaker_id = speaker_id


class book_checkbox(QtWidgets.QCheckBox):
    def __init__(self, parent, book_id):
        super().__init__(parent)
        self.book_id = book_id


class event_manager(Ui_event_manager_window):
    def __init__(self, context):
        super().__init__()
        self.context = context
        self.speaker_checkboxes = []
        self.book_checkboxes = []

    def setup(self):
        Ui_event_manager_window.setupUi(self, self.context)
        self._setup_events()
        self._update_books_table()
        self._update_speakers_table()

    def _setup_events(self):
        self.new_event_button.clicked.connect(self._new_event_clicked)
        self.new_speaker_button.clicked.connect(self._new_speaker_clicked)

    def _new_event_clicked(self):
        if not self.theme_edit.text():
            return
        temp_date = self.dateEdit.date()
        event_date = temp_date.toPyDate()
        if event_date <= datetime.datetime.today().date():
            return
        s_ids = []
        for s in self.speaker_checkboxes:
            if s.isChecked():
                s_ids.append(s.speaker_id)
        if not s_ids:
            return
        b_ids = []
        for b in self.book_checkboxes:
            if b.isChecked():
                b_ids.append(b.book_id)

        self.context.db_client.new_event(self.theme_edit.text(),
                                         event_date,
                                         s_ids,
                                         b_ids)
        self._update_speakers_table()
        self._update_books_table()
        self.theme_edit.setText("")
        self.dateEdit.clear()

    def _new_speaker_clicked(self):
        if not self.phone_edit.text():
            return
        if not self.email_edit.text():
            return
        if not self.name_edit.text():
            return
        if not self.password_edit.text():
            return
        self.context.db_client.new_speaker(self.phone_edit.text(),
                                           self.email_edit.text(),
                                           self.name_edit.text(),
                                           self.password_edit.text())
        self.name_edit.setText("")
        self.phone_edit.setText("")
        self.email_edit.setText("")
        self.password_edit.setText("")

    def _update_speakers_table(self):
        table = self.sp_table
        table.setRowCount(0)
        self.speaker_checkboxes.clear()
        speaker_column = 0
        checkbox_column = 1
        sps = self.context.db_client.speakers
        for s_name, s_id in sps.items():
            row_num = table.rowCount()
            table.insertRow(row_num)

            table.setItem(row_num, speaker_column, create_item(s_name))
            cb = speaker_checkbox(table, s_id)
            table.setCellWidget(row_num, checkbox_column, cb)
            self.speaker_checkboxes.append(cb)

    def _update_books_table(self):
        table = self.b_table
        table.setRowCount(0)
        self.speaker_checkboxes.clear()
        speaker_column = 0
        checkbox_column = 1
        bs = self.context.db_client.books
        for b in bs:
            row_num = table.rowCount()
            table.insertRow(row_num)

            table.setItem(row_num, speaker_column, create_item(b.name))
            cb = book_checkbox(table, b.id)
            table.setCellWidget(row_num, checkbox_column, cb)
            self.book_checkboxes.append(cb)
