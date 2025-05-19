import json
import pathlib
import sqlite3

ROOT = pathlib.Path(__file__).resolve().parents[1]   # carpeta raíz del repo
DB_FILE   = ROOT / "olist.db"
SQL_FILE  = ROOT / "delivery_date_difference.sql"
JSON_FILE = ROOT / "query_results" / "delivery_date_difference.json"

def fetch_query_result():
    """Ejecuta el SQL y devuelve una lista de dicts."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row        # para obtener dict‐like rows
    with open(SQL_FILE, encoding="utf-8") as f:
        query = f.read()
    rows = [dict(r) for r in conn.execute(query)]
    conn.close()
    return rows

def test_delivery_date_difference():
    """Compara resultado real vs. esperado."""
    obtained  = fetch_query_result()

    with open(JSON_FILE, encoding="utf-8") as f:
        expected = json.load(f)

    # ❶ Ordena para que no influyan posiciones si el SQL no tiene ORDER BY
    obtained_sorted  = sorted(obtained , key=lambda x: (x["State"]))
    expected_sorted  = sorted(expected , key=lambda x: (x["State"]))

    # ❷ Si hay floats y quieres tolerancia, cámbialo por assert_almost_equal, etc.
    assert obtained_sorted == expected_sorted