import pytest
from services.database import DatabaseService

MOVIMENTACAO_EXEMPLO = (
    "arquivo.txt",
    ".txt",
    "Documentos",
    "C:/origem",
    "C:/destino/arquivo.txt",
    "2026-07-08T10:00:00",
)

class TestDatabaseService:

    def test_cria_banco_e_tabela_automaticamente(self, tmp_path):
        """Deve criar o arquivo do banco e a tabela na inicialização."""
        caminho = str(tmp_path / "subpasta" / "novo.db")
        db = DatabaseService(caminho_db=caminho)
        db.close()

        import os
        assert os.path.exists(caminho)

    def test_total_movimentacoes_banco_vazio(self, db):
        """Deve retornar 0 para um banco recém-criado."""
        assert db.total_movimentacoes() == 0

    def test_salvar_movimentacao_incrementa_total(self, db):
        """Após salvar uma movimentação, total deve ser 1."""
        db.salvar_movimentacao(*MOVIMENTACAO_EXEMPLO)

        assert db.total_movimentacoes() == 1

    def test_salvar_movimentacoes_em_lote(self, db):
        """Inserção em lote deve salvar todos os registros corretamente."""
        movimentacoes = [
            ("a.txt", ".txt", "Documentos", "/orig", "/dest/a.txt", "2026-07-08T10:00:00"),
            ("b.jpg", ".jpg", "Imagens",    "/orig", "/dest/b.jpg", "2026-07-08T10:01:00"),
            ("c.pdf", ".pdf", "Documentos", "/orig", "/dest/c.pdf", "2026-07-08T10:02:00"),
        ]
        db.salvar_movimentacoes_em_lote(movimentacoes)

        assert db.total_movimentacoes() == 3

    def test_ultimas_movimentacoes_retorna_limite(self, db):
        """Deve retornar no máximo o número de registros solicitado."""
        movimentacoes = [
            (f"arquivo_{i}.txt", ".txt", "Documentos", "/orig", f"/dest/{i}.txt", f"2026-07-08T10:0{i}:00")
            for i in range(5)
        ]
        db.salvar_movimentacoes_em_lote(movimentacoes)

        resultado = db.ultimas_movimentacoes(limite=3)

        assert len(resultado) == 3

    def test_ultimas_movimentacoes_ordem_decrescente(self, db):
        """Deve retornar as movimentações mais recentes primeiro."""
        db.salvar_movimentacao("primeiro.txt", ".txt", "Documentos", "/orig", "/dest/primeiro.txt", "2026-07-08T08:00:00")
        db.salvar_movimentacao("ultimo.txt",   ".txt", "Documentos", "/orig", "/dest/ultimo.txt",   "2026-07-08T10:00:00")

        resultado = db.ultimas_movimentacoes(limite=2)

        assert resultado[0][0] == "ultimo.txt"
        assert resultado[1][0] == "primeiro.txt"

    def test_estatisticas_por_categoria(self, db):
        """Deve agrupar e contar corretamente por categoria."""
        movimentacoes = [
            ("a.txt", ".txt", "Documentos", "/orig", "/dest/a.txt", "2026-07-08T10:00:00"),
            ("b.txt", ".txt", "Documentos", "/orig", "/dest/b.txt", "2026-07-08T10:01:00"),
            ("c.jpg", ".jpg", "Imagens",    "/orig", "/dest/c.jpg", "2026-07-08T10:02:00"),
        ]
        db.salvar_movimentacoes_em_lote(movimentacoes)

        estatisticas = dict(db.estatisticas_por_categoria())

        assert estatisticas["Documentos"] == 2
        assert estatisticas["Imagens"] == 1

    def test_context_manager_fecha_conexao(self, tmp_path):
        """Deve fechar a conexão corretamente ao sair do bloco with."""
        import sqlite3
        caminho = str(tmp_path / "ctx.db")

        with DatabaseService(caminho_db=caminho) as db:
            db.salvar_movimentacao(*MOVIMENTACAO_EXEMPLO)

        with pytest.raises(Exception):
            db.total_movimentacoes()

    def test_gerar_relatorio_sem_erro(self, db):
        """gerar_relatorio() deve executar sem lançar exceção."""
        db.salvar_movimentacao(*MOVIMENTACAO_EXEMPLO)

        db.gerar_relatorio()  # não deve lançar exceção