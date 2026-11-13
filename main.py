"""Single entry point / quickstart."""
import argparse
import sys
from pathlib import Path

# Dynamically add the root directory to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.cmn import config
from src.dal import database

def run_queries():
    import sqlite3
    conn = database.get_connection()
    text = config.QUERIES_SQL.read_text(encoding="utf-8")
    for stmt in [s.strip() for s in text.split(";") if s.strip()]:
        body = "\n".join(l for l in stmt.splitlines() if not l.strip().startswith("--")).strip()
        if not body or body.upper().startswith("PRAGMA"):
            continue
        print("\n>>", stmt.splitlines()[0] if stmt.startswith("--") else body.splitlines()[0])
        try:
            cur = conn.execute(body)
            rows = cur.fetchall()
            if cur.description:
                print("  ", [d[0] for d in cur.description])
                for r in rows:
                    print("  ", tuple(r))
            else:
                print("   OK, rows affected:", cur.rowcount)
        except sqlite3.Error as e:
            print("   ERROR:", e)
    conn.commit(); conn.close()

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--reset", action="store_true")
    p.add_argument("--init-only", action="store_true")
    p.add_argument("--queries", action="store_true")
    a = p.parse_args()

    if a.reset:
        database.init_db()
    else:
        database.ensure_db()
    print(f"Database: {config.DB_PATH}")

    if a.queries:
        run_queries()
    elif not a.init_only:
        from src.ui.app import app
        app.run(debug=True, host="127.0.0.1", port=5000)