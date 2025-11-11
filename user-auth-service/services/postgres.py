from os import getenv
from threading import Lock

from psycopg2 import connect


URI = getenv('POSTGRES_URI')


class Database:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.connection = connect(URI)
            self.initialized = True

    def execute_query(self, query, params=None) -> list[tuple]:
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query, params)
                self.connection.commit()
                return cursor.fetchall()
            except Exception as e:
                self.connection.rollback()
                raise e
