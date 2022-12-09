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
