import sqlite3
from dataClass import fileEntry
from datetime import datetime
from pathlib import Path


class Database:
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

            sha256 TEXT

        )
        """)

        self.conn.commit()


    def close(self):
        self.conn.close()
        

    def upsertFile(self, entries):     # Se me ocurrio hacerlo todo en uno para simplificar el código, pero tengo dudas
        for entry in entries:                                        # de lo rompebolas que puede ser en terminar de rendimiento, O(logn(x)) momento

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
                    sha256=row[5]
                )
            )

        return files
    

    def nukeAll(self):
        self.cursor.execute("""
            DELETE FROM files
        """)

    def getFilesWithoutHash(self) -> list[fileEntry]:

        self.cursor.execute("""
            SELECT
                filePath,
                extension,
                size,
                createdAt,
                modifiedAt,
                sha256
            FROM files
            WHERE sha256 IS NULL
        """)

        rows = self.cursor.fetchall()

        entries = []

        for row in rows:

            entries.append(
                fileEntry(
                    filePath=Path(row[0]),
                    extension=row[1],
                    size=row[2],
                    createdAt=datetime.fromisoformat(row[3]),
                    modifiedAt=datetime.fromisoformat(row[4]),
                    sha256=row[5]
                )
            )

        return entries