import sys
import os
import logging
import pytest

from services.database import DatabaseService

sys.path.insert(0, os.path.dirname(__file__))



@pytest.fixture
def logger():
    return logging.getLogger("teste")

@pytest.fixture
def db(tmp_path_factory):
    caminho = str(tmp_path_factory.mktemp("db") / "teste.db")
    database = DatabaseService(caminho_db=caminho)
    yield database
    database.close()

@pytest.fixture
def regras():
    return {
        "Documentos": [".txt", ".pdf"],
        "Imagens":    [".jpg", ".png"],
    }

@pytest.fixture
def criar_arquivo(tmp_path):
    """
    para criar arquivos temporários nos testes.
    recebe caminho que pode ser tmp_path ou uma subpasta e o nome.
    """
    def _criar_arquivo(caminho, nome, conteudo="conteudo"):
        arquivo = caminho / nome
        arquivo.write_text(conteudo, encoding="utf-8")
        return arquivo

    return _criar_arquivo

@pytest.fixture
def criar_pasta(tmp_path):
    """
    para criar pastas temporárias nos testes.
    recebe caminho que pode ser tmp_path ou uma subpasta e o nome.
    """
    def _criar_pasta(tmp_path, nome):
        caminho = tmp_path / nome
        caminho.mkdir(parents=True, exist_ok=True)
        return caminho

    return _criar_pasta