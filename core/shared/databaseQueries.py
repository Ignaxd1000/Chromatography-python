from dataClass import fileEntry


def saveFileToDb(entry: fileEntry, sessionId: int, cursor, conn):

    cursor.execute("""
    INSERT INTO files(
        filePath,
        extension,
        size,
        createdAt,
        modifiedAt,
        sha256
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        str(entry.filePath),
        entry.extension,
        entry.size,
        entry.createdAt.isoformat(),
        entry.modifiedAt.isoformat(),
        entry.sha256
    ))

    conn.commit()
    return("File saved succesfully papu")