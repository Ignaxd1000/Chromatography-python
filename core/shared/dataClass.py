from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

@dataclass
class appConfig:
    dbPath: str

@dataclass
class fileEntry:
    filePath: Path
    extension: str
    size: int
    createdAt: datetime
    modifiedAt: datetime
    scanTime: datetime
    sha256: str | None = None

