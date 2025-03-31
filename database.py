import psycopg2
from psycopg2 import OperationalError

class Database:
    _instance = None  # Хранит единственный экземпляр класса
    _connection = None  # Хранит соединение с базой данных
    _cursor = None  # Хранит курсор

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def connect(self, user, password, dbname='my_postgres', host='localhost', port='5432'):
        if self._connection is None:
            try:
                self._connection = psycopg2.connect(
                    dbname=dbname,
                    user=user,
                    password=password,
                    host=host,
                    port=port
                )
                print("Подключение к базе данных установлено.")
            except OperationalError as e:
                print(f"Ошибка подключения к базе данных: {e}")

    def open_cursor(self):
        if self._connection and not self._cursor:
            self._cursor = self._connection.cursor()
            print("Курсор открыт.")

    def close_cursor(self):
        if self._cursor:
            self._cursor.close()
            self._cursor = None
            print("Курсор закрыт.")

    def disconnect(self):
        if self._connection:
            self.close_cursor()
            self._connection.close()
            self._connection = None
            print("Отключение от базы данных выполнено.")

    def execute_query(self, query, params=None):
        if self._cursor:
            try:
                self._cursor.execute(query, params or ())
                print("Запрос выполнен успешно.")
            except OperationalError as e:
                print(f"Ошибка выполнения запроса: {e}")

    def fetch_all(self):
        if self._cursor:
            return self._cursor.fetchall()
        return []

    def fetch_one(self):
        if self._cursor:
            return self._cursor.fetchone()
        return None

    def commit(self):
        if self._connection:
            self._connection.commit()
            print("Транзакция подтверждена.")

    def rollback(self):
        if self._connection:
            self._connection.rollback()
            print("Транзакция откачена.")

    def is_connected(self):
        if self._connection:
            return True
        else:
            return False










