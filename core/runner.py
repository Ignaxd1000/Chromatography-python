from shared.database import database
from shared.config import Config
from scanner import scanDirectory
from hasher import *
from shared.dataClass import *

class runner:

    def __init__(self):
        self.config = Config()
        self.db = database(self.config.cfg.dbPath)
        self.entries = []

    def scan(self):
        try:
            self.entries = scanDirectory(self.config.cfg.scanDir)
        except:
            print("Ocurrió un problemin")

    def hash(self):
        if self.entries.count == 0:
            raise Exception("No hay entradas para hashear")
        hashFiles(self.entries)

    def sync(self):
        print()