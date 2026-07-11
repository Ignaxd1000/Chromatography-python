from hasher import hashFiles
from scanner import scanDirectory
from services import ConfigPort, HasherPort, RepositoryPort, ScannerPort
from shared.config import Config
from shared.dataClass import appConfig, fileEntry
from shared.database import database


class ScannerAdapter(ScannerPort):
    def scan_directory(self, root_path: str) -> list[fileEntry]:
        return scanDirectory(root_path)


class HasherAdapter(HasherPort):
    def hash_entries(self, entries: list[fileEntry]) -> None:
        hashFiles(entries)


class DatabaseRepositoryAdapter(RepositoryPort):
    def __init__(self, db_path: str):
        self.db = database(db_path)

    def save_entries(self, entries: list[fileEntry]) -> None:
        for entry in entries:
            self.db.saveFile(entry)
        self.db.conn.commit()

    def get_all_entries(self) -> list[fileEntry]:
        return self.db.getAllFiles()


class ConfigAdapter(ConfigPort):
    def __init__(self):
        self.config = Config()

    def get(self) -> appConfig:
        return self.config.args

    def set_scan_completed(self) -> None:
        self.config.setScanCompleted()

    def set_scan_pending(self) -> None:
        self.config.setScanPending()
