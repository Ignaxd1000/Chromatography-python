import sqlite3
from dataClass import fileEntry
from datetime import *
from pathlib import Path


class database:
    def __init__(self, dbPath):
        self.conn = sqlite3.connect(dbPath)
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY,

            filePath TEXT UNIQUE,
            extension TEXT,
            size INTEGER,

            createdAt TEXT,
            modifiedAt TEXT,

            sha256 TEXT,

        )
        """)

        self.conn.commit()

    def close(self):
        self.conn.close()
        
    def saveFile(self, entry: fileEntry):     # Se me ocurrio hacerlo todo en uno para simplificar el código, pero tengo dudas
                                                # de lo rompebolas que puede ser en terminar de rendimiento, O(logn(x)) momento

        self.cursor.execute("""
        INSERT INTO files (
            filePath,
            extension,
            size,
            createdAt,
            modifiedAt,
            sha256
        )
        VALUES (?, ?, ?, ?, ?, ?)

        ON CONFLICT(filePath)
        DO UPDATE SET
            size = excluded.size,
            modifiedAt = excluded.modifiedAt,
            sha256 = excluded.sha256
        """, (
            str(entry.filePath),
            entry.extension,
            entry.size,
            entry.createdAt.isoformat(),
            entry.modifiedAt.isoformat(),
            entry.sha256
        ))

        self.conn.commit()


    def getAllFiles(self) -> list[fileEntry]:

        self.cursor.execute("""
            SELECT
                filePath,
                extension,
                size,
                createdAt,
                modifiedAt,
                sha256
            FROM files
        """)

        rows = self.cursor.fetchall()

        files = []

        for row in rows:
            files.append(
                fileEntry(
                    filePath=Path(row[0]),
                    extension=row[1],
                    size=row[2],
                    createdAt=datetime.fromisoformat(row[3]),
                    modifiedAt=datetime.fromisoformat(row[4]),
                    scanTime=datetime.fromisoformat(row[5]),
                    sha256=row[5]
                )
            )

        return files