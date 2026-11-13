"""Data Access Layer - connection management and database bootstrap."""
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from src.cmn import config

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(str(config.DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

@contextmanager
def transaction():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def _run_script(conn, script_path: Path):
    conn.executescript(script_path.read_text(encoding="utf-8"))

def init_db(with_seed=True):
    conn = get_connection()
    try:
        _run_script(conn, config.SCHEMA_SQL)
        if with_seed:
            _run_script(conn, config.SEED_SQL)
        conn.commit()
    finally:
        conn.close()

def ensure_db():
    conn = get_connection()
    try:
        has_movie = conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='Movie'"
        ).fetchone()
    finally:
        conn.close()
    if not has_movie:
        init_db(with_seed=True)