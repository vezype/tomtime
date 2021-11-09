import sqlite3


class SQLRequests:
    def __init__(self, way_to_database: str = 'db.sqlite'):
        self.connection = sqlite3.connect(way_to_database)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()
