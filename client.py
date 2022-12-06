import mysql.connector
import hashlib
from enum import Enum
from book import book


class client_role(Enum):
    unauthorized = 1
    reader = 2
    speaker = 3
    librarian = 4
    event_manager = 5


def password_hash(password):
    return int(hashlib.sha256(password.encode('utf-8')).hexdigest(), 16) % 10 ** 20


class queries:
    get_account_info = ("SELECT a.phone, a.password "
                        "FROM accounts AS a "
                        "WHERE a.phone = %s "
                        "GROUP BY a.phone, a.password")

    get_reader_info = ("SELECT r.reader_id, r.name, r.email, r.birth_date "
                       "FROM readers AS r "
                       "WHERE r.phone = %s "
                       "GROUP BY r.reader_id, r.name, r.email, r.birth_date")

    get_speaker_info = ("SELECT s.speaker_id, s.name, s.email "
                        "FROM speakers AS s "
                        "WHERE s.phone = %s "
                        "GROUP BY s.speaker_id, s.name, s.email")

    get_employee_info = ("SELECT e.employee_id, s.spec_id, s.name "
                         "FROM specializations AS s "
                         "INNER JOIN employees AS e ON s.spec_id = e.spec_id "
                         "WHERE e.phone = %s "
                         "GROUP BY e.employee_id, s.spec_id, s.name")

    get_last_reader_id = "SELECT MAX(reader_id) FROM readers"

    insert_account_step1 = ("INSERT INTO accounts "
                            "(phone, password) "
                            "VALUES (%s, %s)")

    insert_account_step2 = ("INSERT INTO readers "
                            "(reader_id, phone, name) "
                            "VALUES (%s, %s, %s)")

    update_account_info = ("UPDATE readers "
                           "SET name = %s, email = %s "
                           "WHERE phone = %s")

    update_password = ("UPDATE accounts "
                       "SET password = %s "
                       "WHERE phone = %s")

    get_all_books_id_name = ("SELECT book_id, name "
                             "FROM books")

    get_book_authors = ("SELECT a.name "
                        "FROM authors AS a "
                        "INNER JOIN `book authors` AS ba ON a.author_id = ba.author_id "
                        "WHERE ba.book_id = %s")

    get_book_genres = ("SELECT g.name "
                       "FROM genres AS g "
                       "INNER JOIN `book genres` AS bg ON g.genre_id = bg.genre_id "
                       "WHERE bg.book_id = %s")

    get_book_instance_by_book_id = ("SELECT bi.book_instance_id "
                                    "FROM `book instance` AS bi "
                                    "WHERE bi.is_available = TRUE and bi.book_id = %s "
                                    "LIMIT 1")

    reserve_book_instance = ("UPDATE `book instance` "
                             "SET is_available = FALSE "
                             "WHERE book_instance_id = %s")

    restore_book_instance = ("UPDATE `book instance` "
                             "SET is_available = TRUE "
                             "WHERE book_instance_id = %s")

    get_last_order_id = "SELECT MAX(order_id) FROM orders"

    create_order_step1 = ("INSERT INTO orders "
                          "(order_id, reader_id, return_date, status_id) "
                          "VALUES (%s, %s, %s, 1)")

    create_order_step2 = ("INSERT INTO `order details` "
                          "(order_id, book_instance_id) "
                          "VALUES (%s, %s)")


class db_client:
    def __init__(self):
        self._connection = mysql.connector.connect(user='root', database='library')
        self.role = client_role.unauthorized
        self.password = None
        self.id = None
        self.name = None
        self.phone = None
        self.email = None
        self.birth_date = None
        self.books = []
        self._update_books()

    def _execute_query(self, query, *args):
        cursor = self._connection.cursor(buffered=True)
        cursor.execute(query, args)
        return cursor

    def _update_books(self):
        books = self._execute_query(queries.get_all_books_id_name)
        for (book_id, name) in books:
            self.books.append(book(book_id, name))

        for b in self.books:
            authors = self._execute_query(queries.get_book_authors, b.id)
            for author, in authors:
                b.authors.append(author)

            genres = self._execute_query(queries.get_book_genres, b.id)
            for genre, in genres:
                b.genres.append(genre)

    def login(self, login, password):
        error_message = None

        account = self._execute_query(queries.get_account_info, login)
        if account.rowcount == 0:
            error_message = "No such user, please create account"
            return error_message

        (phone, hashed_password) = account.fetchone()
        if password_hash(password) == int(hashed_password):
            self.password = password
            self._get_account_info(phone)
        else:
            error_message = "Wrong password, try again"
        return error_message

    def _get_account_info(self, phone):
        self.phone = phone
        reader = self._execute_query(queries.get_reader_info, phone)
        if reader.rowcount:
            (reader_id, name, email, birth_date) = reader.fetchone()
            self.role = client_role.reader
            self.id = int(reader_id)
            self.name = name
            self.email = email
            self.birth_date = birth_date
            return

        speaker = self._execute_query(queries.get_speaker_info, phone)
        if speaker.rowcount:
            (speaker_id, name, email) = speaker.fetchone()
            self.role = client_role.speaker
            self.id = int(speaker_id)
            self.name = name
            self.email = email
            return

        employee = self._execute_query(queries.get_employee_info, phone)
        if employee.rowcount:
            (employee_id, spec_id, name) = employee.fetchone()
            if int(spec_id) == 1:
                self.role = client_role.librarian
            else:
                self.role = client_role.event_manager
            self.id = employee_id
            self.name = name
            return

    def create_account(self, name, phone, password):
        account_exists = self._execute_query(queries.get_account_info, phone).rowcount == 1
        if account_exists:
            return "Account already exists"

        # insert into accounts
        data_to_insert = (phone, password_hash(password))
        cursor = self._connection.cursor(buffered=True)
        cursor.execute(queries.insert_account_step1, data_to_insert)

        # insert into readers
        reader_id, = self._execute_query(queries.get_last_reader_id).fetchone()
        reader_id += 1
        data_to_insert = (reader_id, phone, name)
        cursor = self._connection.cursor(buffered=True)
        cursor.execute(queries.insert_account_step2, data_to_insert)

        # commit data
        self._connection.commit()

        return None

    def update_account_info(self, new_name="", new_email="", new_password=""):
        if new_name:
            self.name = new_name
        if new_email:
            self.email = new_email
        if new_password:
            self.password = new_password

        info = (self.name, self.email, self.phone)
        cursor = self._connection.cursor(buffered=True)
        cursor.execute(queries.update_account_info, info)

        info = (password_hash(self.password), self.phone)
        cursor = self._connection.cursor(buffered=True)
        cursor.execute(queries.update_password, info)

        self._connection.commit()

    def create_order(self, new_order, return_date):
        order = []
        for book_id in new_order:
            b = self._execute_query(queries.get_book_instance_by_book_id, book_id)
            if not b.rowcount:
                for bk in self.books:
                    if bk.id == book_id:
                        return f"Book '{bk.name}' isn't available"

            book_instance_id, = b.fetchone()
            order.append(book_instance_id)

        new_order_id, = self._execute_query(queries.get_last_reader_id).fetchone()
        new_order_id += 1

        cursor = self._connection.cursor(buffered=True)
        data_to_insert = (new_order_id, self.id, return_date)
        cursor.execute(queries.create_order_step1, data_to_insert)

        for book_instance_id in order:
            data_to_insert = (new_order_id, book_instance_id)
            cursor.execute(queries.create_order_step2, data_to_insert)
            cursor.execute(queries.reserve_book_instance, (book_instance_id,))

        self._connection.commit()
        return ""
