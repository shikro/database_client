import datetime
from ui.reader.ui_reader import Ui_reader_window
from PyQt6 import QtWidgets, QtCore


def create_item(text):
    item = QtWidgets.QTableWidgetItem(text)
    item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
    return item


class books_table_button(QtWidgets.QPushButton):
    def __init__(self, parent, book_id, book_name, context):
        super().__init__(parent)
        self.book_id = book_id
        self.book_name = book_name
        self.context = context
        self.setText("add")
        self.clicked.connect(self._clicked)

    def _clicked(self):
        self.context.add_book_to_order(self.book_id, self.book_name)


class orders_table_button(QtWidgets.QPushButton):
    def __init__(self, parent, order_id, context):
        super().__init__(parent)
        self.order_id = order_id
        self.context = context
        self.setText("cancel order")
        self.clicked.connect(self._clicked)

    def _clicked(self):
        self.context.cancel_order(self.order_id)


class all_events_table_button(QtWidgets.QPushButton):
    def __init__(self, parent, event_id, context):
        super().__init__(parent)
        self.event_id = event_id
        self.contex = context
        self.setText("sign up")
        self.clicked.connect(self._clicked)

    def _clicked(self):
        self.contex.sign_up_for_event(self.event_id)


class my_events_table_button(QtWidgets.QPushButton):
    def __init__(self, parent, event_id, context):
        super().__init__(parent)
        self.event_id = event_id
        self.contex = context
        self.setText("won't go")
        self.clicked.connect(self._clicked)

    def _clicked(self):
        self.contex.unsubscribe_from_event(self.event_id)


class reader_window(Ui_reader_window):
    def __init__(self, context):
        super().__init__()
        self.context = context
        self.selected_books = []

    def setup(self):
        Ui_reader_window.setupUi(self, self.context)
        self._setup_account_info_fields()
        self._setup_books_table()
        self._setup_orders_table()
        self._setup_events_table(self.context.db_client.all_events,
                                 self.all_events_table,
                                 all_events_table_button)
        self._setup_events_table(self.context.db_client.get_my_events_info(),
                                 self.my_events_table,
                                 my_events_table_button)
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

            add_to_order_button = books_table_button(self.books_table, book.id, book.name, self)
            self.books_table.setCellWidget(row_num, 0, add_to_order_button)

    def _setup_orders_table(self):
        self.orders_table.setRowCount(0)
        orders = self.context.db_client.orders
        return_date_column = 0
        books_column = 1
        status_column = 2
        button_column = 3
        for order in orders:
            row_num = self.orders_table.rowCount()
            self.orders_table.insertRow(row_num)

            self.orders_table.setItem(row_num, return_date_column, create_item(str(order.return_date)))
            self.orders_table.setItem(row_num, status_column, create_item(order.status))

            book_names_list = QtWidgets.QListWidget()
            self.orders_table.setCellWidget(row_num, books_column, book_names_list)
            for book_name in order.book_names:
                book_names_list.addItem(book_name)

            if order.status == 'Создан':
                cancel_button = orders_table_button(self.orders_table, order.id, self)
                self.orders_table.setCellWidget(row_num, button_column, cancel_button)

    def _setup_events_table(self, source, table, btn_creation_fn ):
        table.setRowCount(0)
        events = source
        theme_column = 0
        speakers_column = 1
        books_column = 2
        date_column = 3
        button_column = 4
        for event in events:
            row_num = table.rowCount()
            table.insertRow(row_num)

            table.setItem(row_num, theme_column, create_item(event.theme))
            table.setItem(row_num, date_column, create_item(str(event.date)))

            speakers_list = QtWidgets.QListWidget()
            table.setCellWidget(row_num, speakers_column, speakers_list)
            for speaker_name in event.speakers:
                speakers_list.addItem(speaker_name)

            books_list = QtWidgets.QListWidget()
            table.setCellWidget(row_num, books_column, books_list)
            for book_name in event.books:
                books_list.addItem(book_name)

            btn = btn_creation_fn(table, event.id, self)
            table.setCellWidget(row_num, button_column, btn)

    def sign_up_for_event(self, event_id):
        if event_id not in self.context.db_client.my_events_id:
            self.context.db_client.sign_up_for_event(event_id)
            self._setup_events_table(self.context.db_client.all_events,
                                     self.all_events_table,
                                     all_events_table_button)
            self._setup_events_table(self.context.db_client.get_my_events_info(),
                                     self.my_events_table,
                                     my_events_table_button)

    def unsubscribe_from_event(self, event_id):
        self.context.db_client.unsubscribe_from_event(event_id)
        self._setup_events_table(self.context.db_client.all_events,
                                 self.all_events_table,
                                 all_events_table_button)
        self._setup_events_table(self.context.db_client.get_my_events_info(),
                                 self.my_events_table,
                                 my_events_table_button)

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

    def cancel_order(self, order_id):
        self.context.db_client.cancel_order(order_id)
        self._setup_orders_table()
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
        print()
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
