from database import cursor, conn
from dataClass import fileEntry


def saveFileToDb(entry: fileEntry, sessionId: int):

    cursor.execute("""
    INSERT INTO files(
        filePath,
        extension,
        size,
        createdAt,
        modifiedAt,
        sha256,
        sessionId
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        str(entry.filePath),
        entry.extension,
        entry.size,
        entry.createdAt.isoformat(),
        entry.modifiedAt.isoformat(),
        entry.sha256,
        sessionId
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