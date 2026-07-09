import sqlite3
from dataClass import fileEntry

class database:
    def __init__(self, dbPath):
        self.conn = sqlite3.connect(dbPath)
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY,

            filePath TEXT,
            extension TEXT,
            size INTEGER,

            createdAt TEXT,
            modifiedAt TEXT,

            sha256 TEXT,
            isDeleted INTEGER DEFAULT 0,
            sessionId INTEGER,

        )
        """)

        self.conn.commit()

    def closeDatabase(self):
        self.conn.close()
        return("Database session succesfully closed:")
        