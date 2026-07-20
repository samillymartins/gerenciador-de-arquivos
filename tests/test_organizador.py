import os
import logging
import pytest

from services.organizador import Organizador
from services.database import DatabaseService

@pytest.fixture
def organizador(tmp_path, regras, logger, db):
    return Organizador(
        pasta_alvo=str(tmp_path),
        regras=regras,
        logger=logger,
        database=db)

class TestInicializacao:

    def test_estatisticas_iniciam_zeradas(self, organizador):
        """Contadores devem estar zerados antes de qualquer execução."""
        assert organizador.processados == 0
        assert organizador.movidos == 0
        assert organizador.ignorados == 0
        assert organizador.erros == 0
        assert organizador.estatisticas == {}

    def test_mapa_extensoes_construido_corretamente(self, organizador):
        """mapa_extensoes deve mapear extensão -> pasta com base nas regras."""
        assert organizador.mapa_extensoes[".txt"] == "Documentos"
        assert organizador.mapa_extensoes[".jpg"] == "Imagens"


class TestListarArquivos:

    def test_lista_arquivos_na_raiz(self, organizador, tmp_path, criar_arquivo):
        """Deve listar arquivos na pasta raiz monitorada."""
        criar_arquivo(tmp_path, "arquivo.txt")

        resultado = list(organizador.listar_arquivos())

        assert len(resultado) == 1

    def test_ignora_pastas_de_categoria(self, organizador, tmp_path):
        """Não deve varrer as pastas de destino definidas nas regras."""
        pasta_doc = tmp_path / "Documentos"
        pasta_doc.mkdir()
        (pasta_doc / "arquivo.txt").write_text("conteudo")

        resultado = list(organizador.listar_arquivos())

        assert resultado == []

    def test_lista_arquivos_recursivamente(self, organizador, tmp_path, criar_arquivo):
        """Deve varrer subpastas que não sejam pastas de categoria."""
        subpasta = tmp_path / "subpasta"
        subpasta.mkdir()
        criar_arquivo(subpasta, "arquivo.txt")

        resultado = list(organizador.listar_arquivos())

        assert len(resultado) == 1

class TestOrganizar:
    def test_move_arquivo_para_categoria_correta(self, organizador, tmp_path, criar_arquivo):
        """Arquivo .txt deve ser movido para a pasta Documentos."""
        criar_arquivo(tmp_path, "relatorio.txt")

        organizador.organizar()

        assert (tmp_path / "Documentos" / "relatorio.txt").exists()

    def test_incrementa_contador_movidos(self, organizador, tmp_path, criar_arquivo):
        """movidos deve refletir o número de arquivos organizados."""
        criar_arquivo(tmp_path, "a.txt")
        criar_arquivo(tmp_path, "b.pdf")

        organizador.organizar()

        assert organizador.movidos == 2

    def test_extensao_desconhecida_incrementa_ignorados(self, organizador, tmp_path, criar_arquivo):
        """Arquivo com extensão fora das regras deve incrementar ignorados."""
        criar_arquivo(tmp_path, "arquivo.xyz")

        organizador.organizar()

        assert organizador.ignorados == 1
        assert organizador.movidos == 0

    def test_arquivo_nao_sobrescreve_existente_no_destino(self, organizador, tmp_path, criar_arquivo):
        """Se já existe arquivo com mesmo nome no destino, deve gerar nome único."""
        criar_arquivo(tmp_path, "relatorio.txt", "versao 1")
        pasta_doc = tmp_path / "Documentos"
        pasta_doc.mkdir()
        (pasta_doc / "relatorio.txt").write_text("versao existente")

        organizador.organizar()

        arquivos = list(pasta_doc.iterdir())
        assert len(arquivos) == 2

    def test_salva_movimentacoes_no_banco(self, organizador, tmp_path, db, criar_arquivo):
        """Movimentações devem ser persistidas no banco de dados."""
        criar_arquivo(tmp_path, "a.txt")
        criar_arquivo(tmp_path, "b.jpg")

        organizador.organizar()

        assert db.total_movimentacoes() == 2

    def test_estatisticas_por_categoria(self, organizador, tmp_path, criar_arquivo):
        """estatisticas deve contar arquivos movidos por categoria."""
        criar_arquivo(tmp_path, "a.txt")
        criar_arquivo(tmp_path, "b.pdf")
        criar_arquivo(tmp_path, "c.jpg")

        organizador.organizar()

        assert organizador.estatisticas["Documentos"] == 2
        assert organizador.estatisticas["Imagens"] == 1


class TestProcessar:
    def test_processar_executa_fluxo_completo(self, organizador, tmp_path, criar_arquivo):
        """processar() deve detectar duplicados, organizar e gerar relatório."""
        criar_arquivo(tmp_path, "original.txt", "conteudo texto")
        criar_arquivo(tmp_path, "copia.txt",    "conteudo texto")  # duplicado de original.txt
        criar_arquivo(tmp_path, "foto.jpg",     "conteudo imagem") # conteúdo diferente, não é duplicado

        organizador.processar()

        assert (tmp_path / "Imagens" / "foto.jpg").exists()
        assert organizador.duplicate_service.duplicados_encontrados == 1