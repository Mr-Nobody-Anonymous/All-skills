import sqlite3
class SQLiteHandler:
    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
