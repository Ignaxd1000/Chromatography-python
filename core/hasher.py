import hashlib
from shared.dataClass import fileEntry
from concurrent.futures import ThreadPoolExecutor, as_completed
import os


def calculateFileHash(entry: fileEntry):

    sha256 = hashlib.sha256()

    with open(entry.filePath, "rb") as f:

        while chunk := f.read(8192):
            sha256.update(chunk)

    entry.sha256 = sha256.hexdigest()


def hashFiles(entries: list[fileEntry], progress):
    with ThreadPoolExecutor(max_workers=max(1, round((os.cpu_count() or 1) / 2))) as executor:   # Hashear es una tarea re jodida para la cpu, imaginate que tenes 70.000 cosas
        futures = [executor.submit(calculateFileHash, e) for e in entries]                       # y tenes que identificar todo, yo me largaria a llorar 

        for completed, future in enumerate(as_completed(futures), start=1):
            future.result()     # El resultado es irrelevante acá, pero si no pongo esto las excepciones no saltan
            progress.step()
