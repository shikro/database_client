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
        self._connection = mysql.connector.connect(user='root', database='library')
        self.role = client_role.unauthorized
        self.id = None
        self.name = None
        self.phone = None
        self.email = None
        self.birth_date = None

    def _execute_query(self, query):
        cursor = self._connection.cursor(buffered=True)
        cursor.execute(query)
        return cursor

    def login(self, login, password):
        error_message = None
        query = (f"SELECT a.phone, a.password "
                 f"FROM accounts AS a "
                 f"WHERE a.phone = '{login}' "
                 f"GROUP BY a.phone, a.password")
        account = self._execute_query(query)

        if account.rowcount == 0:
            error_message = "No such user, please create account"
            return error_message

        (phone, hashed_password) = account.fetchone()
        if password_hash(password) == int(hashed_password):
            self.get_account_info(phone)
        else:
            error_message = "Wrong password, try again"
        return error_message

    def get_account_info(self, phone):
        check_readers = (f"SELECT r.reader_id, r.name, r.email, r.birth_date "
                         f"FROM readers AS r "
                         f"WHERE r.phone = '{phone}' "
                         f"GROUP BY r.reader_id, r.name, r.email, r.birth_date")
        reader = self._execute_query(check_readers)
        if reader.rowcount:
            (reader_id, name, email, birth_date) = reader.fetchone()
            self.role = client_role.reader
            self.id = int(reader_id)
            self.name = name
            self.email = email
            self.birth_date = birth_date
            return

        check_speakers = (f"SELECT s.speaker_id, s.name, s.email "
                          f"FROM speakers AS s "
                          f"WHERE s.phone = '{phone}' "
                          f"GROUP BY s.speaker_id, s.name, s.email")
        speaker = self._execute_query(check_speakers)
        if speaker.rowcount:
            (speaker_id, name, email) = speaker.fetchone()
            self.role = client_role.speaker
            self.id = int(speaker_id)
            self.name = name
            self.email = email
            return

        check_employees = (f"SELECT e.employee_id, s.spec_id, s.name "
                           f"FROM specializations AS s "
                           f"INNER JOIN employees AS e ON s.spec_id = e.spec_id "
                           f"WHERE e.phone = '{phone}' "
                           f"GROUP BY e.employee_id, s.spec_id, s.name")
        employee = self._execute_query(check_employees)
        if employee.rowcount:
            (employee_id, spec_id, name) = employee.fetchone()
            if int(spec_id) == 1:
                self.role = client_role.librarian
            else:
                self.role = client_role.event_manager
            self.id = employee_id
            self.name = name
            return
