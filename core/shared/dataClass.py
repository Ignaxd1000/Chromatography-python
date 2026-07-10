from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

@dataclass
class appConfig:
    dbPath: str
    scanDir: str
    isScanCompleted: bool

@dataclass
class fileEntry:
    filePath: Path
    extension: str
    size: int
    createdAt: datetime
    modifiedAt: datetime
    sha256: str | None = None

