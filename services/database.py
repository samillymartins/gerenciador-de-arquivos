import sqlite3
import os


class DatabaseService:

    def __init__(self):
        os.makedirs("database", exist_ok=True)
        self.conexao = sqlite3.connect("database/organizador.db")
        self.criar_tabela()

    def criar_tabela(self):

        cursor = self.conexao.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movimentacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                arquivo TEXT NOT NULL,
                extensao TEXT NOT NULL,
                categoria TEXT NOT NULL,
                origem TEXT NOT NULL,
                destino TEXT NOT NULL,
                data_movimentacao DATETIME NOT NULL
            )
        """)

        self.conexao.commit()

    def salvar_movimentacao(self, arquivo, extensao, categoria, origem, destino, data_movimentacao):

        cursor = self.conexao.cursor()

        cursor.execute("""
            INSERT INTO movimentacoes (
                arquivo,
                extensao,
                categoria,
                origem,
                destino,
                data_movimentacao
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, 
        (arquivo, extensao, categoria, origem, destino, data_movimentacao))

        self.conexao.commit()