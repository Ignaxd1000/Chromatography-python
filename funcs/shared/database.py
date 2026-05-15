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

    isDeleted INTEGER,

    sessionId INTEGER,

    FOREIGN KEY(sessionId)
        REFERENCES scanSessions(id)
)
""")

conn.commit()

conn.commit()

def saveFileToDb(entry: fileEntry):
    cursor.execute("""
    INSERT INTO files(
        filePath,
        extension,
        size,
        createdAt,
        modifiedAt,
        scanTime,
        sha256,
        isDeleted
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        str(entry.filePath),
        entry.extension,
        entry.size,
        entry.createdAt.isoformat(),
        entry.modifiedAt.isoformat(),
        entry.sha256
    ))

    conn.commit()

def createScanSession(scanTime: str, rootPath: str):

    cursor.execute("""
    INSERT INTO scanSessions(
        scanTime,
        rootPath
    )
    VALUES (?, ?)
    """, (
        scanTime,
        rootPath
    ))

    conn.commit()

    return cursor.lastrowid