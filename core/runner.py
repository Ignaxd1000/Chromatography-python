from shared.database import database
from shared.config import Config
from scanner import scanDirectory
from hasher import hashFiles
from shared.dataClass import *
from shared.exceptions import *


class runner:

    def __init__(self):
        self.config = Config()
        self.database = database(self.config.args.dbPath)
        self.entries = []

    def save(self):
        if not self.entries:
            raise Exception("No hay entradas para guardar")
        for entry in self.entries:
            self.database.saveFile(entry)
        self.database.conn.commit()     # Ya sé que esto deberia ir en el database.py, pero si lo pongo ahí hago un commit
                                        # por cada iteración del for, no hace falta que explique más supongo.


    def scan(self):
        if self.config.args.isScanCompleted:
            raise scanAlreadyCompleted()
        
        self.config.setScanPending()
        try:
            self.entries = scanDirectory(self.config.args.scanDir)
            self.save()
            self.config.setScanCompleted()
        except Exception as e:
            print(f"Ocurrió un problemin. {e}")


    def sync(self):
        self.entries = self.database.getAllFiles()


    def hash(self):
        self.sync()
        if not self.entries:
            raise Exception("No hay entradas para hashear")
        
        hashFiles(self.entries)
        try:
            self.save()
        except Exception as e:
            print(f"Ocurrió un problemin. {e}")

        