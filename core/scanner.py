from shared.dataClass import fileEntry
from datetime import datetime
from pathlib import Path


def scanDirectory(rootPath: Path) -> list[fileEntry]:

    entries = []

    for file in rootPath.rglob("*"):

        if not file.is_file():
            continue

        stats = file.stat()

        entry = fileEntry(
            filePath=file,
            extension=file.suffix,
            size=stats.st_size,

            scanTime=datetime.now(),

            createdAt=datetime.fromtimestamp(
                stats.st_ctime
            ),

            modifiedAt=datetime.fromtimestamp(
                stats.st_mtime
            )
        )

        entries.append(entry)

    return entries
