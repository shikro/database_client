from PyQt6 import QtWidgets, QtCore
from ui.librarian.ui_librarian import Ui_librarian_window


def create_item(text):
    item = QtWidgets.QTableWidgetItem(text)
    item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
    return item


class author_checkbox(QtWidgets.QCheckBox):
    def __init__(self, parent, author_id):
        super().__init__(parent)
        self.author_id = author_id


class genre_checkbox(QtWidgets.QCheckBox):
    def __init__(self, parent, genre_id):
        super().__init__(parent)
        self.genre_id = genre_id


class on_create_widget(QtWidgets.QDialogButtonBox):
    def __init__(self, order_id, context):
        super().__init__()
        self.order_id = order_id
        self.context = context
        apply_button = QtWidgets.QPushButton(self.tr("&apply"))
        apply_button.setDefault(True)
        reject_button = QtWidgets.QPushButton(self.tr("&reject"))
        self.addButton(apply_button, QtWidgets.QDialogButtonBox.ButtonRole.AcceptRole)
        self.addButton(reject_button, QtWidgets.QDialogButtonBox.ButtonRole.RejectRole)
        self.accepted.connect(self._acp_emitted)
        self.rejected.connect(self._rej_emitted)

    def _acp_emitted(self):
        self.context.accept_order(self.order_id)

    def _rej_emitted(self):
        self.context.reject_order(self.order_id)


class orders_button(QtWidgets.QPushButton):
    def __init__(self, text, order_id, context):
        super().__init__()
        self.clicked.connect(self._clicked)
        self.setText(text)
        self.order_id = order_id
        self.context = context

    def _clicked(self):
        self.context.issue_order(self.order_id)


class on_close_widget(QtWidgets.QDialogButtonBox):
    def __init__(self, order_id, context):
        super().__init__()
        self.order_id = order_id
        self.context = context
        apply_button = QtWidgets.QPushButton(self.tr("&close"))
        apply_button.setDefault(True)
        reject_button = QtWidgets.QPushButton(self.tr("&penalty"))
        self.addButton(apply_button, QtWidgets.QDialogButtonBox.ButtonRole.AcceptRole)
        self.addButton(reject_button, QtWidgets.QDialogButtonBox.ButtonRole.RejectRole)
        self.accepted.connect(self._acp_emitted)
        self.rejected.connect(self._rej_emitted)

    def _acp_emitted(self):
        self.context.close_order(self.order_id)

    def _rej_emitted(self):
        self.context.check_penalty(self.order_id)


class librarian_window(Ui_librarian_window):
    def __init__(self, context):
        super().__init__()
        self.context = context
        self.author_checkboxes = []
        self.genre_checkboxes = []

    def setup(self):
        Ui_librarian_window.setupUi(self, self.context)
        self._setup_events()
        self._update_authors_table()
        self._update_genre_table()
        self._update_book_combobox()
        self._update_condition_combobox()
        self._update_book_to_remove_combobox()
        self._update_new_bi_id()
        self._update_orders_table()

    def _setup_events(self):
        self.add_book_button.clicked.connect(self._add_book_clicked)
        self.add_author_button.clicked.connect(self._add_author_clicked)
        self.add_genre_button.clicked.connect(self._add_genre_clicked)
        self.add_book_instance_button.clicked.connect(self._add_book_instance_clicked)
        self.remove_book_button.clicked.connect(self._remove_book_instance_clicked)
        return

    def _add_author_clicked(self):
        if not self.author_name_edit.text():
            return
        self.context.db_client.new_author(self.author_name_edit.text())
        self.author_name_edit.setText("")

    def _add_genre_clicked(self):
        if not self.genre_name_edit.text():
            return
        self.context.db_client.new_genre(self.genre_name_edit.text())
        self.genre_name_edit.setText("")

    def _add_book_clicked(self):
        if not self.book_name_edit.text():
            return
        b_name = self.book_name_edit.text()

        a_ids = []
        for acb in self.author_checkboxes:
            if acb.isChecked():
                a_ids.append(acb.author_id)
        if not a_ids:
            return

        g_ids = []
        for gcb in self.genre_checkboxes:
            if gcb.isChecked():
                g_ids.append(gcb.genre_id)
        if not g_ids:
            return

        p = int(self.slider_label.text())

        self.context.db_client.new_book(b_name, a_ids, g_ids, p)
        self._update_book_combobox()
        self._update_authors_table()
        self._update_genre_table()
        self.book_name_edit.setText("")

    def _add_book_instance_clicked(self):
        b_id = int(self.book_id_combobox.currentText())
        c = self.condition_combobox.currentText()
        self.context.db_client.new_book_instance(b_id, c)
        self._update_new_bi_id()
        self._update_book_to_remove_combobox()

    def _remove_book_instance_clicked(self):
        b_id = int(self.book_to_remove_combobox.currentText())
        self.context.db_client.remove_book_instance(b_id)
        self._update_book_to_remove_combobox()
        self._update_new_bi_id()

    def _update_authors_table(self):
        self.authors_table.setRowCount(0)
        self.author_checkboxes.clear()
        authors_column = 0
        checkbox_column = 1
        authors = self.context.db_client.authors
        for author_name, author_id in authors.items():
            row_num = self.authors_table.rowCount()
            self.authors_table.insertRow(row_num)

            self.authors_table.setItem(row_num, authors_column, create_item(author_name))
            cb = author_checkbox(self.authors_table, author_id)
            self.authors_table.setCellWidget(row_num, checkbox_column, cb)
            self.author_checkboxes.append(cb)

    def _update_genre_table(self):
        self.genres_table.setRowCount(0)
        self.genre_checkboxes.clear()
        genre_column = 0
        checkbox_column = 1
        genres = self.context.db_client.genres
        for genre_name, genre_id in genres.items():
            row_num = self.genres_table.rowCount()
            self.genres_table.insertRow(row_num)

            self.genres_table.setItem(row_num, genre_column, create_item(genre_name))
            cb = genre_checkbox(self.genres_table, genre_id)
            self.genres_table.setCellWidget(row_num, checkbox_column, cb)
            self.genre_checkboxes.append(cb)

    def _update_book_combobox(self):
        self.book_id_combobox.clear()
        books = self.context.db_client.books
        for book in books:
            self.book_id_combobox.addItem(str(book.id))

    def _update_condition_combobox(self):
        self.condition_combobox.clear()
        for cond, _ in self.context.db_client.book_conditions.items():
            self.condition_combobox.addItem(cond)

    def _update_book_to_remove_combobox(self):
        self.book_to_remove_combobox.clear()
        for b_id in self.context.db_client.book_instance_ids:
            self.book_to_remove_combobox.addItem(str(b_id))

    def _update_new_bi_id(self):
        self.bi_id_label.setText(str(self.context.db_client.get_id_for_new_bi()))

    def _update_orders_table(self):
        self.pending_orders_table.setRowCount(0)
        for order in self.context.db_client.orders:
            row_num = self.pending_orders_table.rowCount()
            self.pending_orders_table.insertRow(row_num)

            self.pending_orders_table.setItem(row_num, 0, create_item(str(order.id)))
            order_bi_ids_list = QtWidgets.QListWidget()
            self.pending_orders_table.setCellWidget(row_num, 1, order_bi_ids_list)
            for i in order.book_ids:
                order_bi_ids_list.addItem(str(i))
            self.pending_orders_table.setItem(row_num, 2, create_item(order.status))
            match order.status:
                case 'Создан':
                    cell_widget = on_create_widget(order.id, self)
                case 'Готов к выдаче':
                    cell_widget = orders_button("issue", order.id, self)
                case 'Ожидает сдачи':
                    cell_widget = on_close_widget(order.id, self)
                case _:
                    cell_widget = QtWidgets.QWidget()

            self.pending_orders_table.setCellWidget(row_num, 3, cell_widget)

    def accept_order(self, order_id):
        self.context.db_client.accept_order(order_id)
        self._update_orders_table()

    def reject_order(self, order_id):
        self.context.db_client.reject_order(order_id)
        self._update_orders_table()

    def issue_order(self, order_id):
        print("iss" + str(order_id))
        self.context.db_client.issue_order(order_id)
        self._update_orders_table()

    def close_order(self, order_id):
        self.context.db_client.close_order(order_id)
        self.penalty_label.setText("")
        self._update_orders_table()

    def check_penalty(self, order_id):
        p = self.context.db_client.check_penalty(order_id)
        self.penalty_label.setText(str(int(p)) + ' rub')
