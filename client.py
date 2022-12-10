import mysql.connector
import hashlib
from enum import Enum

from book import book
from order import order
from event import event


class client_role(Enum):
    unauthorized = 1
    reader = 2
    speaker = 3
    librarian = 4
    event_manager = 5


def password_hash(password):
    return int(hashlib.sha256(password.encode('utf-8')).hexdigest(), 16) % 10 ** 20


class queries:
    @staticmethod
    def get_account_info(phone):
        return ("SELECT a.phone, a.password "
                "FROM accounts AS a "
                f"WHERE a.phone = '{phone}' "
                "GROUP BY a.phone, a.password")

    @staticmethod
    def get_reader_info(phone):
        return ("SELECT r.reader_id, r.name, r.email, r.birth_date "
                "FROM readers AS r "
                f"WHERE r.phone = '{phone}' "
                "GROUP BY r.reader_id, r.name, r.email, r.birth_date")

    @staticmethod
    def get_speaker_info(phone):
        return ("SELECT s.speaker_id, s.name, s.email "
                "FROM speakers AS s "
                f"WHERE s.phone = '{phone}' "
                "GROUP BY s.speaker_id, s.name, s.email")

    @staticmethod
    def get_employee_info(phone):
        return ("SELECT e.employee_id, s.spec_id, s.name "
                "FROM specializations AS s "
                "INNER JOIN employees AS e ON s.spec_id = e.spec_id "
                f"WHERE e.phone = '{phone}' "
                "GROUP BY e.employee_id, s.spec_id, s.name")

    @staticmethod
    def get_last_reader_id():
        return "SELECT MAX(reader_id) FROM readers"

    @staticmethod
    def insert_account_step1(phone, password):
        return ("INSERT INTO accounts "
                "(phone, password) "
                f"VALUES ('{phone}', '{password}')")

    @staticmethod
    def insert_account_step2(reader_id, phone, name):
        return ("INSERT INTO readers "
                "(reader_id, phone, name) "
                f"VALUES ({reader_id}, '{phone}', '{name}')")

    @staticmethod
    def update_account_info(name, email, phone):
        return ("UPDATE readers "
                f"SET name = '{name}', email = '{email}' "
                f"WHERE phone = '{phone}'")

    @staticmethod
    def update_password(password, phone):
        return ("UPDATE accounts "
                f"SET password = '{password}' "
                f"WHERE phone = '{phone}'")

    @staticmethod
    def get_all_books_id_name():
        return ("SELECT book_id, name "
                "FROM books")

    @staticmethod
    def get_book_authors(book_id):
        return ("SELECT a.name "
                "FROM authors AS a "
                "INNER JOIN `book authors` AS ba ON a.author_id = ba.author_id "
                f"WHERE ba.book_id = {book_id}")

    @staticmethod
    def get_book_genres(book_id):
        return ("SELECT g.name "
                "FROM genres AS g "
                "INNER JOIN `book genres` AS bg ON g.genre_id = bg.genre_id "
                f"WHERE bg.book_id = {book_id}")

    @staticmethod
    def get_book_instance_by_book_id(book_id):
        return ("SELECT bi.book_instance_id "
                "FROM `book instance` AS bi "
                f"WHERE bi.is_available = TRUE and bi.book_id = {book_id} "
                "LIMIT 1")

    @staticmethod
    def reserve_book_instance(book_instance_id):
        return ("UPDATE `book instance` "
                "SET is_available = FALSE "
                f"WHERE book_instance_id = {book_instance_id}")

    @staticmethod
    def restore_book_instance(book_instance_id):
        return ("UPDATE `book instance` "
                "SET is_available = TRUE "
                f"WHERE book_instance_id = {book_instance_id}")

    @staticmethod
    def get_last_order_id():
        return "SELECT MAX(order_id) FROM orders"

    @staticmethod
    def create_order_step1(order_id, reader_id, return_date):
        return ("INSERT INTO orders "
                "(order_id, reader_id, return_date, status_id) "
                f"VALUES ({order_id}, {reader_id}, '{return_date.strftime('%Y-%m-%d %H:%M:%S')}', 1)")

    @staticmethod
    def create_order_step2(order_id, book_instance_id):
        return ("INSERT INTO `order details` "
                "(order_id, book_instance_id) "
                f"VALUES ({order_id}, {book_instance_id})")

    @staticmethod
    def get_order_id_name(reader_id):
        return ("SELECT o.order_id, s.status_name, o.return_date "
                "FROM orders AS o "
                "INNER JOIN statuses AS s ON o.status_id = s.status_id "
                f"WHERE o.reader_id = {reader_id}")

    @staticmethod
    def get_book_names(order_id):
        return f"CALL getOrderBookNames({order_id})"

    @staticmethod
    def cancel_order(order_id):
        return ("UPDATE orders "
                "SET status_id = 4 "
                f"WHERE order_id = {order_id}")

    @staticmethod
    def restore_order_books(order_id):
        return ("UPDATE `book instance` AS bi "
                "INNER JOIN `order details` AS od ON bi.book_instance_id = od.book_instance_id "
                "SET bi.is_available = TRUE "
                f"WHERE od.order_id = {order_id}")

    @staticmethod
    def get_events_id_date_theme():
        return ("SELECT e.event_id, e.`date`, e.theme "
                "FROM events AS e")

    @staticmethod
    def get_event_speakers(event_id):
        return ("SELECT s.speaker_id, s.name "
                "FROM speakers AS s "
                "INNER JOIN `event speakers` AS es ON es.speaker_id = s.speaker_id "
                f"WHERE es.event_id = {event_id}")

    @staticmethod
    def get_event_books(event_id):
        return ("SELECT b.name "
                "FROM books AS b "
                "INNER JOIN  `event books` AS eb ON b.book_id = eb.book_id "
                f"WHERE eb.event_id = {event_id}")

    @staticmethod
    def get_my_events(reader_id):
        return ("SELECT el.event_id "
                "FROM `event listeners` AS el "
                "INNER JOIN readers AS r ON r.reader_id = el.reader_id "
                f"WHERE r.reader_id = {reader_id}")

    @staticmethod
    def sign_up_for_event(event_id, reader_id):
        return ("INSERT INTO `event listeners` "
                "(event_id, reader_id) "
                f"VALUES ({event_id}, {reader_id})")

    @staticmethod
    def unsubscribe_from_event(event_id, reader_id):
        return ("DELETE FROM `event listeners` "
                f"WHERE event_id = {event_id} and reader_id = {reader_id}")

    @staticmethod
    def get_last_author_id():
        return "SELECT MAX(author_id) FROM authors"

    @staticmethod
    def get_last_genre_id():
        return "SELECT MAX(genre_id) FROM genres"

    @staticmethod
    def new_author(name, a_id):
        return ("INSERT INTO authors "
                "(author_id, name) "
                f"VALUES ({a_id}, '{name}')")

    @staticmethod
    def new_genre(name, g_id):
        return ("INSERT INTO genres "
                "(genre_id, name) "
                f"VALUES ({g_id}, '{name}')")

    @staticmethod
    def get_last_book_instance_id():
        return "SELECT MAX(book_instance_id) FROM `book instance`"

    @staticmethod
    def new_book_instance(bi_id, b_id, c_id):
        return ("INSERT INTO `book instance` "
                "(book_instance_id, book_id, condition_id, is_available) "
                f"VALUES ({bi_id}, {b_id}, {c_id}, 1)")

    @staticmethod
    def is_book_instance_available(bi_id):
        return ("SELECT 1 "
                "FROM `book instance` "
                f"WHERE book_instance_id = {bi_id} and is_available = TRUE")

    @staticmethod
    def get_last_book_id():
        return "SELECT MAX(book_id) FROM books"

    @staticmethod
    def new_book(b_id, name, pen):
        return ("INSERT INTO books "
                "(book_id, name, penalty_per_day) "
                f"VALUES ({b_id}, '{name}', {pen})")

    @staticmethod
    def add_author_to_book(b_id, a_id):
        return ("INSERT INTO `book authors` "
                "(book_id, author_id) "
                f"VALUES ({b_id}, {a_id})")

    @staticmethod
    def add_genre_to_book(b_id, g_id):
        return ("INSERT INTO `book genres`"
                "(book_id, genre_id) "
                f"VALUES ({b_id}, {g_id})")

    @staticmethod
    def get_authors_id_name():
        return ("SELECT * "
                "FROM authors")

    @staticmethod
    def get_genres_id_name():
        return ("SELECT * "
                "FROM genres")

    @staticmethod
    def get_conditions():
        return ("SELECT * "
                "FROM conditions")

    @staticmethod
    def get_available_bi():
        return ("SELECT book_instance_id "
                "FROM `book instance` "
                "WHERE is_available = TRUE")

    @staticmethod
    def get_all_orders():
        return "CALL getAllOrders()"

    @staticmethod
    def accept_order(order_id):
        return ("UPDATE orders "
                "SET status_id = 2 "
                f"WHERE order_id = {order_id}")

    @staticmethod
    def issue_order(order_id):
        return ("UPDATE orders "
                "SET status_id = 3 "
                f"WHERE order_id = {order_id}")

    @staticmethod
    def close_order(order_id):
        return ("UPDATE orders "
                "SET status_id = 5 "
                f"WHERE order_id = {order_id}")

    @staticmethod
    def get_penalty(order_id):
        return f"CALL getOrderPenalties({order_id})"

    @staticmethod
    def get_speakers_id_name():
        return ("SELECT speaker_id, name "
                "FROM speakers")

    @staticmethod
    def get_last_event_id():
        return "SELECT MAX(event_id) FROM events"

    @staticmethod
    def get_last_speaker_id():
        return "SELECT MAX(speaker_id) FROM speakers"

    @staticmethod
    def new_event(e_id, date, theme):
        return ("INSERT INTO events "
                "(event_id, `date`, theme) "
                f"VALUES ({e_id}, '{date.strftime('%Y-%m-%d %H:%M:%S')}', '{theme}')")

    @staticmethod
    def add_speaker_to_event(s_id, e_id):
        return ("INSERT INTO `event speakers` "
                "(event_id, speaker_id) "
                f"VALUES ({e_id}, {s_id})")

    @staticmethod
    def new_speaker(s_id, phone, name, email):
        return ("INSERT INTO speakers "
                "(speaker_id, phone, name, email) "
                f"VALUES ({s_id}, '{phone}', '{name}', '{email}')")

    @staticmethod
    def add_book_to_event(b_id, e_id):
        return ("INSERT INTO `event books` "
                "(event_id, book_id) "
                f"VALUES ({e_id}, {b_id})")

    @staticmethod
    def event_id_by_speaker(s_id):
        return ("SELECT e.event_id "
                "FROM events AS e "
                "INNER JOIN `event speakers` AS es ON e.event_id = es.event_id "
                f"WHERE es.speaker_id = {s_id}")


class db_client:
    def __init__(self):
        self._connection = mysql.connector.connect(user='root',
                                                   password='',
                                                   host='127.0.0.1',
                                                   port='3306',
                                                   database='library')
        self.role = client_role.unauthorized
        self.password = None
        self.id = None
        self.name = None
        self.phone = None
        self.email = None
        self.birth_date = None
        self.books = []
        self.orders = []
        self.authors = {}
        self.genres = {}
        self.book_conditions = {}
        self.book_instance_ids = []
        self.all_events = []
        self.my_events_id = []
        self.speakers = {}

    def _execute_query(self, query, *args):
        while not self._connection.is_connected():
            self._connection.reconnect()
        cursor = self._connection.cursor(buffered=True)
        cursor.execute(query, args)
        return cursor

    def _update_books(self):
        self.books.clear()
        books = self._execute_query(queries.get_all_books_id_name())
        for (book_id, name) in books:
            self.books.append(book(book_id, name))

        for b in self.books:
            authors = self._execute_query(queries.get_book_authors(b.id))
            for author, in authors:
                b.authors.append(author)

            genres = self._execute_query(queries.get_book_genres(b.id))
            for genre, in genres:
                b.genres.append(genre)

    def _update_orders(self):
        self.orders.clear()
        orders = self._execute_query(queries.get_order_id_name(reader_id=self.id))
        for (order_id, order_status, return_date) in orders:
            new_order = order(order_id, order_status)
            new_order.return_date = return_date
            book_names = self._execute_query(queries.get_book_names(order_id=order_id))
            for (book_name, bi_id) in book_names:
                new_order.book_names.append(book_name)
                new_order.book_ids.append(bi_id)

            self.orders.append(new_order)

    def cancel_order(self, order_id):
        for o in self.orders:
            if o.id == order_id:
                if not o.status == 'Создан':
                    return

        self._execute_query(queries.cancel_order(order_id))
        self._execute_query(queries.restore_order_books(order_id))
        self._connection.commit()
        self._update_orders()

    def _update_all_events(self):
        self.all_events.clear()
        events = self._execute_query(queries.get_events_id_date_theme())
        for (event_id, event_date, event_theme) in events:
            new_event = event(event_id)
            new_event.date = event_date
            new_event.theme = event_theme

            speakers = self._execute_query(queries.get_event_speakers(event_id))
            for (_, speaker_name) in speakers:
                new_event.speakers.append(speaker_name)

            books = self._execute_query(queries.get_event_books(event_id))
            for book_name, in books:
                new_event.books.append(book_name)

            self.all_events.append(new_event)

    def sign_up_for_event(self, event_id):
        self._execute_query(queries.sign_up_for_event(event_id, self.id))
        self._connection.commit()
        self._update_my_events()

    def unsubscribe_from_event(self, event_id):
        self._execute_query(queries.unsubscribe_from_event(event_id, self.id))
        self._connection.commit()
        self._update_my_events()

    def _update_my_events(self):
        self.my_events_id.clear()
        events = self._execute_query(queries.get_my_events(self.id))
        for event_id, in events:
            self.my_events_id.append(event_id)

    def get_my_events_info(self):
        my_events_info = []
        for event_id in self.my_events_id:
            for ev in self.all_events:
                if ev.id == event_id:
                    my_events_info.append(ev)

        return my_events_info

    def login(self, login, password):
        error_message = None

        account = self._execute_query(queries.get_account_info(login))
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
        reader = self._execute_query(queries.get_reader_info(phone))
        if reader.rowcount:
            (reader_id, name, email, birth_date) = reader.fetchone()
            self.role = client_role.reader
            self.id = int(reader_id)
            self.name = name
            self.email = email
            self.birth_date = birth_date
            self._update_all_events()
            self._update_my_events()
            self._update_orders()
            self._update_books()
            return

        speaker = self._execute_query(queries.get_speaker_info(phone))
        if speaker.rowcount:
            (speaker_id, name, email) = speaker.fetchone()
            self.role = client_role.speaker
            self.id = int(speaker_id)
            self.name = name
            self.email = email
            self._update_all_events()
            self._update_sp_events()
            return

        employee = self._execute_query(queries.get_employee_info(phone))
        if employee.rowcount:
            (employee_id, spec_id, name) = employee.fetchone()
            self.id = employee_id
            self.name = name
            if int(spec_id) == 1:
                self.role = client_role.librarian
                self._update_books()
                self._update_authors()
                self._update_genres()
                self._update_conditions()
                self._update_book_instances()
                self._update_all_orders()
            else:
                self.role = client_role.event_manager
                self._update_books()
                self._update_speakers()
            return

    def create_account(self, name, phone, password):
        account_exists = self._execute_query(queries.get_account_info(phone)).rowcount == 1
        if account_exists:
            return "Account already exists"

        # insert into accounts
        cursor = self._connection.cursor(buffered=True)
        cursor.execute(queries.insert_account_step1(phone, password_hash(password)))

        # insert into readers
        reader_id, = self._execute_query(queries.get_last_reader_id()).fetchone()
        reader_id += 1
        cursor = self._connection.cursor(buffered=True)
        cursor.execute(queries.insert_account_step2(reader_id, phone, name))

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

        cursor = self._connection.cursor(buffered=True)
        cursor.execute(queries.update_account_info(self.name, self.email, self.phone))

        cursor = self._connection.cursor(buffered=True)
        cursor.execute(queries.update_password(password_hash(self.password), self.phone))

        self._connection.commit()

    def create_order(self, new_order, return_date):
        order = []
        for book_id in new_order:
            b = self._execute_query(queries.get_book_instance_by_book_id(book_id))
            if not b.rowcount:
                for bk in self.books:
                    if bk.id == book_id:
                        return f"Book '{bk.name}' isn't available"

            book_instance_id, = b.fetchone()
            order.append(book_instance_id)

        new_order_id, = self._execute_query(queries.get_last_order_id()).fetchone()
        new_order_id += 1

        cursor = self._connection.cursor(buffered=True)
        cursor.execute(queries.create_order_step1(new_order_id, self.id, return_date))

        for book_instance_id in order:
            cursor.execute(queries.create_order_step2(new_order_id, book_instance_id))
            cursor.execute(queries.reserve_book_instance(book_instance_id))

        self._connection.commit()
        self._update_orders()
        return ""

    def _update_authors(self):
        authors = self._execute_query(queries.get_authors_id_name())
        for a_id, a_name in authors:
            self.authors[a_name] = a_id

    def _update_genres(self):
        genres = self._execute_query(queries.get_genres_id_name())
        for g_id, g_name in genres:
            self.genres[g_name] = g_id

    def _update_book_instances(self):
        self.book_instance_ids.clear()
        bi_ids = self._execute_query(queries.get_available_bi())
        for bi_id, in bi_ids:
            self.book_instance_ids.append(bi_id)

    def _update_conditions(self):
        conditions = self._execute_query(queries.get_conditions())
        for cond_id, cond_name in conditions:
            self.book_conditions[cond_name] = cond_id

    def get_id_for_new_bi(self):
        bi_id, = self._execute_query(queries.get_last_book_instance_id()).fetchone()
        bi_id += 1
        return bi_id

    def new_author(self, name):
        a_id, = self._execute_query(queries.get_last_author_id()).fetchone()
        a_id += 1
        self._execute_query(queries.new_author(name, a_id))
        self._connection.commit()
        self._update_authors()

    def new_genre(self, name):
        g_id, = self._execute_query(queries.get_last_genre_id()).fetchone()
        g_id += 1
        self._execute_query(queries.new_genre(name, g_id))
        self._connection.commit()
        self._update_genres()

    def new_book(self, name, author_ids, genre_ids, penalty):
        b_id, = self._execute_query(queries.get_last_book_id()).fetchone()
        b_id += 1
        self._execute_query(queries.new_book(b_id, name, penalty))
        self._connection.commit()
        for a_id in author_ids:
            self._execute_query(queries.add_author_to_book(b_id, a_id))
        for g_id in genre_ids:
            self._execute_query(queries.add_genre_to_book(b_id, g_id))
        self._connection.commit()
        self._update_books()

    def new_book_instance(self, book_id, condition):
        bi_id, = self._execute_query(queries.get_last_book_instance_id()).fetchone()
        bi_id += 1
        c_id = self.book_conditions[condition]
        self._execute_query(queries.new_book_instance(bi_id, book_id, c_id))
        self._connection.commit()
        self._update_book_instances()

    def remove_book_instance(self, book_id):
        if self._execute_query(queries.is_book_instance_available(book_id)).rowcount == 0:
            return

        self._execute_query(queries.reserve_book_instance(book_id))
        self._connection.commit()
        self._update_book_instances()

    def _update_all_orders(self):
        self.orders.clear()
        orders = self._execute_query(queries.get_all_orders())
        for (order_id, order_status, return_date) in orders:
            new_order = order(order_id, order_status)
            new_order.return_date = return_date
            book_names = self._execute_query(queries.get_book_names(order_id=order_id))
            for (book_name, bi_id) in book_names:
                new_order.book_names.append(book_name)
                new_order.book_ids.append(bi_id)

            self.orders.append(new_order)

    def accept_order(self, order_id):
        self._execute_query(queries.accept_order(order_id))
        self._connection.commit()
        self._update_all_orders()

    def reject_order(self, order_id):
        self._execute_query(queries.cancel_order(order_id))
        self._execute_query(queries.restore_order_books(order_id))
        self._connection.commit()
        self._update_all_orders()

    def issue_order(self, order_id):
        self._execute_query(queries.issue_order(order_id))
        self._connection.commit()
        self._update_all_orders()

    def check_penalty(self, order_id):
        penalties = self._execute_query(queries.get_penalty(order_id))
        penalty = 0
        for (_, _, p) in penalties:
            if p > 0:
                penalty += p
        return penalty

    def close_order(self, order_id):
        self._execute_query(queries.close_order(order_id))
        self._execute_query(queries.restore_order_books(order_id))
        self._connection.commit()
        self._update_all_orders()

    def _update_speakers(self):
        self.speakers.clear()
        sps = self._execute_query(queries.get_speakers_id_name())
        for (s_id, s_name) in sps:
            self.speakers[s_name] = s_id

    def new_speaker(self, phone, email, name, password):
        s_id, = self._execute_query(queries.get_last_speaker_id()).fetchone()
        s_id += 1
        self._execute_query(queries.insert_account_step1(phone, password_hash(password)))
        self._connection.commit()
        self._execute_query(queries.new_speaker(s_id, phone, name, email))
        self._connection.commit()
        self._update_speakers()

    def new_event(self, theme, date, speakers, books):
        e_id, = self._execute_query(queries.get_last_event_id()).fetchone()
        e_id += 1
        self._execute_query(queries.new_event(e_id, date, theme))
        self._connection.commit()
        for s in speakers:
            self._execute_query(queries.add_speaker_to_event(s, e_id))
        for b in books:
            self._execute_query(queries.add_book_to_event(b, e_id))
        self._connection.commit()

    def _update_sp_events(self):
        self.my_events_id.clear()
        events = self._execute_query(queries.event_id_by_speaker(self.id))
        for event_id, in events:
            self.my_events_id.append(event_id)
