from shared.database import database
from shared.config import Config
from scanner import scanDirectory
from hasher import *
from shared.dataClass import *

class runner:

    def __init__(self):
        self.config = Config()
        self.database = database(self.config.args.dbPath)
        self.entries = []

    def scan(self):
        try:
            self.entries = scanDirectory(self.config.args.scanDir)
        except Exception as e:
            print(f"Ocurrió un problemin. {e}")

    def hash(self):
        if self.entries.count == 0:
            raise Exception("No hay entradas para hashear")
        hashFiles(self.entries)

    def sync(self):
        print()

    def save(self):
        if self.entries.count == 0:
            raise Exception("No hay entradas para guardar")
        for entry in self.entries:
            self.database.__saveFile(entry)
        