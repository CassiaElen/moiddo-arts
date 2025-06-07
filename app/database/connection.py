import sqlite3
from contextlib import contextmanager

class DB:
    def __init__(self, db_name="moiddo_arts.db"):
        self.db_name = db_name

    @contextmanager
    def get_conn(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

db = DB()
