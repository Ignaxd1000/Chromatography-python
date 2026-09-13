from __future__ import annotations

import sqlite3
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MAIN_PATH = REPO_ROOT / "main.py"


def _run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(MAIN_PATH), *args],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )


def test_scan_command_persists_records_and_prints_summary(tmp_path: Path) -> None:
    scan_dir = tmp_path / "scan"
    scan_dir.mkdir()
    (scan_dir / "a.txt").write_text("alpha", encoding="utf-8")
    (scan_dir / "b.log").write_text("beta", encoding="utf-8")

    db_path = tmp_path / "test.db"
    result = _run_cli("--scan", str(scan_dir), "--db", str(db_path))

    assert result.returncode == 0
    assert "Scan completed: 2 records saved" in result.stdout

    with sqlite3.connect(db_path) as conn:
        rows = conn.execute("SELECT filePath FROM files").fetchall()
    assert len(rows) == 2


def test_fetch_command_prints_all_records(tmp_path: Path) -> None:
    db_path = tmp_path / "seeded.db"
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE files (
                id INTEGER PRIMARY KEY,
                filePath TEXT UNIQUE,
                extension TEXT,
                size INTEGER,
                createdAt TEXT,
                modifiedAt TEXT,
                sha256 TEXT
            )
            """
        )
        conn.execute(
            """
            INSERT INTO files (filePath, extension, size, createdAt, modifiedAt, sha256)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            ("/tmp/a.txt", ".txt", 10, "2026-01-01T00:00:00", "2026-01-02T00:00:00", None),
        )
        conn.execute(
            """
            INSERT INTO files (filePath, extension, size, createdAt, modifiedAt, sha256)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            ("/tmp/b.bin", ".bin", 20, "2026-01-01T00:00:00", "2026-01-03T00:00:00", "abc"),
        )
        conn.commit()

    result = _run_cli("--fetch", "--db", str(db_path))

    assert result.returncode == 0
    assert "Fetched 2 records" in result.stdout
    assert "path=/tmp/a.txt" in result.stdout
    assert "path=/tmp/b.bin" in result.stdout


def test_scan_invalid_path_returns_nonzero_with_message(tmp_path: Path) -> None:
    db_path = tmp_path / "test.db"
    result = _run_cli("--scan", str(tmp_path / "missing"), "--db", str(db_path))

    assert result.returncode != 0
    assert "does not exist or is not a directory" in result.stderr


def test_invalid_or_missing_args_return_nonzero() -> None:
    result_no_args = _run_cli()
    assert result_no_args.returncode != 0
    assert "usage:" in result_no_args.stderr.lower()

    result_both_flags = _run_cli("--scan", ".", "--fetch")
    assert result_both_flags.returncode != 0
    assert "not allowed with argument" in result_both_flags.stderr.lower()
