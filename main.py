from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
CORE_DIR = ROOT_DIR / "core"
SHARED_DIR = CORE_DIR / "shared"

for p in (CORE_DIR, SHARED_DIR):
    p_str = str(p)
    if p_str not in sys.path:
        sys.path.insert(0, p_str)

from scanner import scanDirectory
from hasher import hashFiles
from shared.database import Database
from shared.progress import taskProgress


def _default_db_path() -> str:
    config_path = ROOT_DIR / "assets" / "conf.json"
    if not config_path.exists():
        return str(ROOT_DIR / "assets" / "cases" / "chromatography.db")

    with open(config_path, "r", encoding="utf-8") as config_file:
        data = json.load(config_file)

    return data.get("dbPath", str(ROOT_DIR / "assets" / "cases" / "chromatography.db"))


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="chroma")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--scan", metavar="PATH", help="Scan a directory and store records in DB")
    group.add_argument("--fetch", action="store_true", help="Fetch all records from DB")
    group.add_argument("--hash", action="store_true", help="Hash DB records missing sha256")
    parser.add_argument(
        "--db",
        default=_default_db_path(),
        help="Path to sqlite database (defaults to value from assets/conf.json)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    db_path = Path(args.db)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    if args.scan:
        scan_path = Path(args.scan)
        if not scan_path.exists() or not scan_path.is_dir():
            print(f"Scan path does not exist or is not a directory: {scan_path}", file=sys.stderr)
            return 1

        database = Database(str(db_path))
        try:
            entries = scanDirectory(scan_path)
            database.upsertFile(entries)
        finally:
            database.close()

        print(f"Scan completed: {len(entries)} records saved to {db_path}")
        return 0

    database = Database(str(db_path))
    try:
        if args.hash:
            entries = database.getFilesWithoutHash()
            if not entries:
                print(f"No records missing hash in {db_path}")
                return 0

            progress = taskProgress()
            progress.reset(len(entries))
            hashFiles(entries, progress)
            database.upsertFile(entries)
            print(f"Hash completed: {len(entries)} records updated in {db_path}")
            return 0

        entries = sorted(database.getAllFiles(), key=lambda entry: str(entry.filePath))
        print(f"Fetched {len(entries)} records from {db_path}")
        for entry in entries:
            print(
                f"path={entry.filePath} | ext={entry.extension} | size={entry.size} | "
                f"createdAt={entry.createdAt.isoformat()} | modifiedAt={entry.modifiedAt.isoformat()} | "
                f"sha256={entry.sha256}"
            )
        return 0
    finally:
        database.close()


if __name__ == "__main__":
    raise SystemExit(main())