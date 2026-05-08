import sqlite3
import os

class DBConnection:
    def __init__(self, db_path="catatan_harian.db"):
        self.db_path = db_path
        self._init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _init_db(self):
        # Check if schema needs to be initialized
        if not os.path.exists(self.db_path):
            schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
            with open(schema_path, "r") as f:
                schema = f.read()
            
            conn = self.get_connection()
            conn.executescript(schema)
            conn.commit()
            conn.close()
