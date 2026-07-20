import os
import pytest
import logging

from services.duplicate_service import DuplicateService
from core.constants import PASTA_DUPLICADOS

@pytest.fixture
def service(tmp_path, logger):
    return DuplicateService(pasta_alvo=str(tmp_path), logger=logger)

class TestEncontrarDuplicados:

    def test_sem_arquivos_retorna_lista_vazia(self, service):
        """Pasta vazia não deve retornar duplicados."""
        resultado = service.encontrar_duplicados()

        assert resultado == []

    def test_arquivos_unicos_nao_sao_duplicados(self, service, tmp_path, criar_arquivo):
        """Arquivos com conteúdos distintos não devem ser detectados como duplicados."""
        criar_arquivo(tmp_path, "a.txt", "conteudo A")
        criar_arquivo(tmp_path, "b.txt", "conteudo B")

        resultado = service.encontrar_duplicados()

        assert resultado == []

    def test_detecta_arquivos_com_mesmo_conteudo(self, service, tmp_path, criar_arquivo):
        """Dois arquivos com mesmo conteúdo devem ser detectados como duplicados."""
        criar_arquivo(tmp_path, "original.txt", "conteudo igual")
        criar_arquivo(tmp_path, "copia.txt",    "conteudo igual")

        resultado = service.encontrar_duplicados()

        assert len(resultado) == 1

    def test_duplicado_contem_campos_esperados(self, service, tmp_path, criar_arquivo):
        """Cada entrada da lista de duplicados deve conter original, duplicado, hash e tamanho."""
        criar_arquivo(tmp_path, "original.txt", "conteudo")
        criar_arquivo(tmp_path, "copia.txt",    "conteudo")

        resultado = service.encontrar_duplicados()

        assert "original"  in resultado[0]
        assert "duplicado" in resultado[0]
        assert "hash"      in resultado[0]
        assert "tamanho"   in resultado[0]

    def test_atualiza_contador_de_duplicados(self, service, tmp_path, criar_arquivo):
        """duplicados_encontrados deve refletir o número de duplicados detectados."""
        criar_arquivo(tmp_path, "original.txt", "conteudo")
        criar_arquivo(tmp_path, "copia.txt",    "conteudo")

        service.encontrar_duplicados()

        assert service.duplicados_encontrados == 1

    def test_detecta_duplicados_em_subpastas(self, service, tmp_path, criar_arquivo):
        """Duplicados em subpastas devem ser detectados (varredura recursiva)."""
        criar_arquivo(tmp_path, "original.txt", "conteudo")
        subpasta = tmp_path / "subpasta"
        subpasta.mkdir()
        (subpasta / "copia.txt").write_text("conteudo", encoding="utf-8")

        resultado = service.encontrar_duplicados()

        assert len(resultado) == 1

    def test_arquivos_mesmo_nome_conteudo_diferente_nao_sao_duplicados(self, service, tmp_path, criar_arquivo):
        """Arquivos com mesmo nome mas conteúdo diferente não são duplicados."""
        criar_arquivo(tmp_path, "arquivo.txt", "conteudo A")
        subpasta = tmp_path / "subpasta"
        subpasta.mkdir()
        (subpasta / "arquivo.txt").write_text("conteudo B", encoding="utf-8")

        resultado = service.encontrar_duplicados()

        assert resultado == []


class TestMoverDuplicados:

    def test_move_duplicado_para_pasta_duplicados(self, service, tmp_path, criar_arquivo):
        """Arquivo duplicado deve ser movido para a pasta Duplicados."""
        criar_arquivo(tmp_path, "original.txt", "conteudo")
        criar_arquivo(tmp_path, "copia.txt",    "conteudo")

        service.encontrar_duplicados()
        service.mover_para_duplicados()

        pasta_dup = tmp_path / PASTA_DUPLICADOS
        assert pasta_dup.exists()
        assert len(list(pasta_dup.iterdir())) == 1

    def test_incrementa_contador_de_movidos(self, service, tmp_path, criar_arquivo):
        """duplicados_movidos deve ser incrementado após mover."""
        criar_arquivo(tmp_path, "original.txt", "conteudo")
        criar_arquivo(tmp_path, "copia.txt",    "conteudo")

        service.encontrar_duplicados()
        service.mover_para_duplicados()

        assert service.duplicados_movidos == 1

    def test_nao_sobrescreve_arquivo_existente_em_duplicados(self, service, tmp_path, criar_arquivo):
        """Se já existir um arquivo com o mesmo nome em Duplicados, gera nome único."""
        criar_arquivo(tmp_path, "original.txt", "conteudo A")
        criar_arquivo(tmp_path, "copia_1.txt",  "conteudo A")
        criar_arquivo(tmp_path, "copia_2.txt",  "conteudo A")

        service.encontrar_duplicados()
        service.mover_para_duplicados()

        pasta_dup = tmp_path / PASTA_DUPLICADOS
        arquivos = list(pasta_dup.iterdir())
        assert len(arquivos) == 2

    def test_mover_sem_duplicados_nao_lanca_excecao(self, service):
        """Chamar mover_para_duplicados() sem duplicados não deve lançar exceção."""
        service.mover_para_duplicados()