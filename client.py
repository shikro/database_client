import mysql.connector
import hashlib
from enum import Enum


class client_role(Enum):
    unauthorized = 1
    reader = 2
    speaker = 3
    librarian = 4
    event_manager = 5


def password_hash(password):
    return int(hashlib.sha256(password.encode('utf-8')).hexdigest(), 16) % 10 ** 20


class db_client:
    def __init__(self):
        self.connection = mysql.connector.connect(user='root', database='library')
        self.role = client_role.unauthorized

    def execute_query(self, query):
        cursor = self.connection.cursor(buffered=True)
        cursor.execute(query)
        return cursor

    def login(self, login, password):
        query = (f"SELECT a.phone, a.password "
                 f"FROM accounts AS a "
                 f"WHERE a.phone = '{login}' "
                 f"GROUP BY a.phone, a.password")
        result = self.execute_query(query)

        if result.rowcount == 0:
            print("no such user")
            return

        for (phone, hashed_password) in result:
            if password_hash(password) == int(hashed_password):
                self.get_account_info(phone)
                print(self.role)
            else:
                print(f"wrong password {password_hash(password)}")

    def get_account_info(self, phone):
        check_readers = (f"SELECT r.reader_id "
                         f"FROM readers AS r "
                         f"WHERE r.phone = '{phone}' "
                         f"GROUP BY r.reader_id")
        readers = self.execute_query(check_readers)
        if readers.rowcount:
            self.role = client_role.reader
            return

        check_speakers = (f"SELECT s.speaker_id "
                          f"FROM speakers AS s "
                          f"WHERE s.phone = '{phone}' "
                          f"GROUP BY s.speaker_id")
        speakers = self.execute_query(check_speakers)
        if speakers.rowcount:
            self.role = client_role.speaker
            return

        check_employees = (f"SELECT s.spec_id "
                           f"FROM specializations AS s "
                           f"INNER JOIN employees AS e ON s.spec_id = e.spec_id "
                           f"WHERE e.phone = '{phone}' "
                           f"GROUP BY s.spec_id")
        employees = self.execute_query(check_employees)
        if employees.rowcount:
            (spec_id,) = employees.fetchone()
            if int(spec_id) == 1:
                self.role = client_role.librarian
            else:
                self.role = client_role.event_manager
            return
