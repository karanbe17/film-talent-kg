"""Central configuration.
Uses pathlib to calculate absolute paths dynamically at runtime relative to THIS script.
Guarantees the DB is found whether run from root, src/ui, or GitHub Codespaces.
"""
from pathlib import Path

# Calculates the project root by moving 2 levels up from src/cmn/config.py
PROJECT_ROOT = Path(__file__).resolve().parents[2]

SQL_DIR = PROJECT_ROOT / "src" / "dal" / "models" / "relational" / "sql"
SCHEMA_SQL = SQL_DIR / "01_schema.sql"
SEED_SQL = SQL_DIR / "02_seed.sql"
QUERIES_SQL = SQL_DIR / "03_queries.sql"

# Force the database into data/preprocessed/
DB_DIR = PROJECT_ROOT / "data" / "preprocessed"
DB_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DB_DIR / "ProduCast.db"