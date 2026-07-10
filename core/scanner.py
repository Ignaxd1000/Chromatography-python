from shared.dataClass import fileEntry
from datetime import datetime
from pathlib import Path


def scanDirectory(rootPath) -> list[fileEntry]:

    rootPath = Path(rootPath)
    entries = []

    for file in rootPath.rglob("*"):

        if not file.is_file():
            continue

        stats = file.stat()

        entry = fileEntry(
            filePath=file,
            extension=file.suffix,
            size=stats.st_size,


            createdAt=datetime.fromtimestamp(
                stats.st_ctime
            ),

            modifiedAt=datetime.fromtimestamp(
                stats.st_mtime
            )
        )

        entries.append(entry)

    return entries
