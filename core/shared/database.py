import sqlite3
from shared.config import config
from dataClass import fileEntry
conn = sqlite3.connect("config.dbPath")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS scanSessions (
    id INTEGER PRIMARY KEY,

    scanTime TEXT,
    rootPath TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY,

    filePath TEXT,
    extension TEXT,
    size INTEGER,

    createdAt TEXT,
    modifiedAt TEXT,

    sha256 TEXT,
    isDeleted INTEGET DEFAULT 0,
    sessionId INTEGER,

    FOREIGN KEY(sessionId)
        REFERENCES scanSessions(id)
)
""")

conn.commit()