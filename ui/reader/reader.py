import datetime
from ui.reader.ui_reader import Ui_reader_window
from PyQt6 import QtWidgets, QtCore


def create_item(text):
    item = QtWidgets.QTableWidgetItem(text)
    item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
    return item


class table_button(QtWidgets.QPushButton):
    def __init__(self, parent, book_id, book_name, context):
        super().__init__(parent)
        self.book_id = book_id
        self.book_name = book_name
        self.context = context
        self.setText("add")
        self.clicked.connect(self._clicked)

    def _clicked(self):
        self.context.add_book_to_order(self.book_id, self.book_name)


class reader_window(Ui_reader_window):
    def __init__(self, context):
        super().__init__()
        self.context = context
        self.selected_books = []

    def setup(self):
        Ui_reader_window.setupUi(self, self.context)
        self._setup_account_info_fields()
        self._setup_books_table()
        self._setup_events()

    def _setup_account_info_fields(self):
        self.name_edit.setText(self.context.db_client.name)
        self.phone_edit.setText(self.context.db_client.phone)
        self.email_edit.setText(self.context.db_client.email)
        self.password_edit.setText(self.context.db_client.password)

    def _setup_books_table(self):
        books = self.context.db_client.books
        name_column = 1
        authors_column = 2
        genres_column = 3
        for book in books:
            row_num = self.books_table.rowCount()
            self.books_table.insertRow(row_num)

            self.books_table.setItem(row_num, name_column, create_item(book.name))
            authors = ', '.join(map(str, book.authors))
            self.books_table.setItem(row_num, authors_column, create_item(authors))
            genres = ', '.join(map(str, book.genres))
            self.books_table.setItem(row_num, genres_column, create_item(genres))

            add_to_order_button = table_button(self.books_table, book.id, book.name, self)
            self.books_table.setCellWidget(row_num, 0, add_to_order_button)

    def _setup_events(self):
        self.update_info_button.clicked.connect(self._update_info_clicked)
        self.create_order_button.clicked.connect(self._create_order_clicked)
        self.clear_order_button.clicked.connect(self._clear_order_clicked)

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

    def add_book_to_order(self, book_id, book_name):
        self.info_label.setText("")
        if book_id in self.selected_books:
            return
        self.selected_books.append(book_id)
        self.books_in_order_list.addItem(book_name)
        return

    def _create_order_clicked(self):
        if not self.selected_books:
            self.info_label.setText("Please choose at least 1 book")
            return

        temp_date = self.return_date_edit.date()
        return_date = temp_date.toPyDate()
        if return_date <= datetime.datetime.today().date():
            self.info_label.setText("Invalid return date")
            return

        error_message = self.context.db_client.create_order(self.selected_books, return_date)
        if error_message:
            self.books_in_order_list.clear()
            self.selected_books.clear()
            self.info_label.setText(error_message)
            return

        self.books_in_order_list.clear()
        self.selected_books.clear()
        self.info_label.setText("Order created")

    def _clear_order_clicked(self):
        self.info_label.setText("")
        self.selected_books.clear()
        self.books_in_order_list.clear()
