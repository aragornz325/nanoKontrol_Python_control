import sqlite3
from pathlib import Path
import logging
import os
import sys

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [DATABASE] %(message)s")


def resource_path(relative_path):
    return os.path.join(getattr(sys, "_MEIPASS", os.path.abspath(".")), relative_path)


# Ruta a la base de datos empaquetada o en dev
APPDATA_DIR = Path(os.getenv("LOCALAPPDATA")) / "NanoKontrolConfig"
APPDATA_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = APPDATA_DIR / "assignments.sqlite"


def init_db():
    logging.info("Inicializando base de datos...")

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS assignments (
                control_id TEXT PRIMARY KEY,
                action_name TEXT,
                params TEXT
            )
        """
        )


def get_all_assignments():
    logging.info("Obteniendo todas las asignaciones...")
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute(
            "SELECT control_id, action_name, params FROM assignments"
        ).fetchall()


def save_assignment(control_id, action_name, params=""):
    logging.info(f"Guardando asignación: {control_id} -> {action_name} ({params})")
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO assignments (control_id, action_name, params)
            VALUES (?, ?, ?)
            ON CONFLICT(control_id) DO UPDATE SET
                action_name=excluded.action_name,
                params=excluded.params
        """,
            (control_id, action_name, params),
        )
