from shared.database import Database
from shared.config import Config
from scanner import scanDirectory
from hasher import hashFiles
from shared.dataClass import *
from shared.exceptions import *


class Runner:

    def __init__(self):
        self.config = Config()
        self.database = Database(self.config.args.dbPath)
        self.entries = []


    def save(self):
        if not self.entries:
            raise noEntryException()
        self.database.upsertFile(self.entries)


    def scan(self):
        if self.config.args.isScanCompleted:
            raise scanAlreadyCompleted()
        

        try:
            self.entries = scanDirectory(self.config.args.scanDir)
            self.save()
            self.config.setScanCompleted()
        except Exception as e:
            raise e


    def loadDatabaseEntries(self):
        self.entries = self.database.getAllFiles()


    def hash(self):
        entries = self.database.getFilesWithoutHash()
        if not entries:
            raise noEntryException()
        
        hashFiles(entries)
        try:
            for entry in entries:
                self.database.upsertFile(entry)
        except Exception as e:
            raise e


    def editConfig(self, databasePath, scanDirectory, scanState):
        try:
            self.config.edit(appConfig(
                dbPath=databasePath,
                scanDir=scanDirectory,
                isScanCompleted=scanState
            ))
        except Exception as e:
            raise e
        

    def resetCase(self):
        self.database.nukeAll()
        self.config.setScanPending()