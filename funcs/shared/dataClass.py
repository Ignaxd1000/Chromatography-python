from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

@dataclass
class appConfig:
    dbPath: str
    workDirectory: str

@dataclass
class fileEntry:
    filePath: Path
    extension: str
    size: int
    createdAt: datetime
    modifiedAt: datetime
    sha256: str | None
    scanTime: str
    isDeleted: bool
