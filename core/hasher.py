import hashlib
from shared.dataClass import fileEntry

def calculateFileHash(entry: fileEntry):

    sha256 = hashlib.sha256()

    with open(entry.filePath, "rb") as f:

        while chunk := f.read(8192):
            sha256.update(chunk)

    entry.sha256 = sha256.hexdigest()


def hashFiles(entries: list[fileEntry]):

    for entry in entries:
        calculateFileHash(entry)
