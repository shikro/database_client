from ui.speaker.ui_speaker import Ui_speaker_window
from PyQt6 import QtWidgets, QtCore


def create_item(text):
    item = QtWidgets.QTableWidgetItem(text)
    item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
    return item


class speaker_window(Ui_speaker_window):
    def __init__(self, context):
        super().__init__()
        self.context = context

    def setup(self):
        Ui_speaker_window.setupUi(self, self.context)
        self._setup_events_table(self.context.db_client.get_my_events_info(),
                                 self.tableWidget)

    def _setup_events_table(self, source, table):
        table.setRowCount(0)
        events = source
        theme_column = 0
        date_column = 1

        for event in events:
            row_num = table.rowCount()
            table.insertRow(row_num)

            table.setItem(row_num, theme_column, create_item(event.theme))
            table.setItem(row_num, date_column, create_item(str(event.date)))

