import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("reservas.db")

def conectar():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def criar_tabela():
    with conectar() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS reservas (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          laboratorio TEXT NOT NULL,
          responsavel TEXT NOT NULL,
          data TEXT NOT NULL,
          turno TEXT NOT NULL,
          finalidade TEXT NOT NULL,
          status TEXT NOT NULL,
          data_criacao TEXT NOT NULL
        )""")
