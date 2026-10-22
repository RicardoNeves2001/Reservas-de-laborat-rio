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
          data_criacao TEXT NOT NULL,
          quantidade_alunos INTEGER NOT NULL DEFAULT 1
            CHECK (quantidade_alunos BETWEEN 1 AND 40)
        )""")
        columns = {row["name"] for row in conn.execute("PRAGMA table_info(reservas)")}
        if "quantidade_alunos" not in columns:
            conn.execute("""ALTER TABLE reservas
              ADD COLUMN quantidade_alunos INTEGER NOT NULL DEFAULT 1
              CHECK (quantidade_alunos BETWEEN 1 AND 40)""")
