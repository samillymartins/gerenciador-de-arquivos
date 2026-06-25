import sqlite3
import os

class DatabaseService:

    def __init__(self, caminho_db, logger=None):
        self.logger = logger
        
        os.makedirs(os.path.dirname(os.path.abspath(caminho_db)), exist_ok=True)
        
        self.conexao = sqlite3.connect(caminho_db, check_same_thread=False)
        self.criar_tabela()
        
    def close(self):
        self.conexao.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

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

    def total_movimentacoes(self):

        cursor = self.conexao.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM movimentacoes
        """)

        return cursor.fetchone()[0]
    
    def ultimas_movimentacoes(self, limite=10):

        cursor = self.conexao.cursor()

        cursor.execute("""
            SELECT
                arquivo,
                categoria,
                data_movimentacao
            FROM movimentacoes
            ORDER BY data_movimentacao DESC
            LIMIT ?
        """, (limite,))

        return cursor.fetchall()
    
    def estatisticas_por_categoria(self):

        cursor = self.conexao.cursor()

        cursor.execute("""
            SELECT
                categoria,
                COUNT(*)
            FROM movimentacoes
            GROUP BY categoria
            ORDER BY COUNT(*) DESC
        """)

        return cursor.fetchall()
    
    def gerar_relatorio(self):

        print("\n===== RELATÓRIO =====\n")
        print(f"Total movimentações: {self.total_movimentacoes()}")

        print("\nCategorias:")
        for categoria, total in (self.estatisticas_por_categoria()):
            print(f"{categoria}: {total}")

        print("\nÚltimos arquivos:")
        for arquivo, categoria, data in (self.ultimas_movimentacoes()):

            print(
                f"{arquivo} "
                f"({categoria}) "
                f"- {data}"
            )