import sqlite3
from shared.config import config
from dataClass import fileEntry
conn = sqlite3.connect("config.dbPath")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY,
            filePath TEXT,
            extension TEXT,
            size INTEGER,
            createdAt TEXT,
            modifiedAt TEXT,
            scanTime TEXT,
            sha256 TEXT,
            isDeleted INTEGER -- Se me ocurrio mostrar si un archivo fue eliminado, esto lo voy a hacer a lo ultimo porque es como probar que dios no existe
)
""")

conn.commit()

def saveFileToDb(entry: fileEntry): # Hasta ahora meto solo guardado, dsp armo consultas en este mismo archivo
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