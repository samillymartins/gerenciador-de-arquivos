import pytest

from services.cleanup_services import CleanupService
from core.constants import PASTAS_PROTEGIDAS


@pytest.fixture
def service(tmp_path, logger):
    return CleanupService(pasta_alvo=str(tmp_path), logger=logger)

class TestRemoverPastasVazias:

    def test_nao_remove_pasta_alvo(self, service, tmp_path):
        """A pasta raiz monitorada nunca deve ser removida, mesmo estando vazia."""
        service.remover_pastas_vazias()

        assert tmp_path.exists()

    def test_remove_subpasta_vazia(self, service, tmp_path, criar_pasta):
        """Subpasta vazia deve ser removida."""
        subpasta = criar_pasta(tmp_path, "vazia")

        service.remover_pastas_vazias()

        assert not subpasta.exists()

    def test_nao_remove_subpasta_com_arquivos(self, service, tmp_path, criar_arquivo, criar_pasta):
        """Subpasta com arquivos não deve ser removida."""
        subpasta = criar_pasta(tmp_path, "com_arquivos")
        criar_arquivo(subpasta, "arquivo.txt")

        service.remover_pastas_vazias()

        assert subpasta.exists()

    def test_remove_subpasta_vazia_aninhada(self, service, tmp_path, criar_pasta):
        """Subpastas vazias em múltiplos níveis devem ser removidas de dentro para fora."""
        subpasta = criar_pasta(tmp_path, "nivel1/nivel2/nivel3")

        service.remover_pastas_vazias()

        assert not subpasta.exists()
        assert not (tmp_path / "nivel1" / "nivel2").exists()
        assert not (tmp_path / "nivel1").exists()

    def test_nao_remove_pasta_protegida(self, service, tmp_path, criar_pasta):
        """Pastas cujo nome está em PASTAS_PROTEGIDAS não devem ser removidas,
        mesmo estando vazias."""
        for nome in PASTAS_PROTEGIDAS:
            criar_pasta(tmp_path, nome)

        service.remover_pastas_vazias()

        for nome in PASTAS_PROTEGIDAS:
            assert (tmp_path / nome).exists(), f"Pasta protegida '{nome}' foi removida indevidamente"

    def test_remove_apenas_pastas_vazias_entre_mistas(self, service, tmp_path, criar_arquivo, criar_pasta):
        """Quando há pastas vazias e não vazias no mesmo nível, só as vazias
        devem ser removidas."""
        vazia = criar_pasta(tmp_path, "vazia")
        com_arquivo = criar_pasta(tmp_path, "com_arquivo")
        criar_arquivo(com_arquivo, "arquivo.txt")

        service.remover_pastas_vazias()

        assert not vazia.exists()
        assert com_arquivo.exists()

    def test_pasta_vazia_dentro_de_protegida_nao_e_removida(self, service, tmp_path, criar_pasta):
        """Subpastas dentro de uma pasta protegida não devem ser tocadas,
        pois o os.walk não entra nelas (topdown=False respeita o skip do basename)."""
        nome_protegido = next(iter(PASTAS_PROTEGIDAS))
        subpasta_interna = criar_pasta(tmp_path, f"{nome_protegido}/interna_vazia")

        service.remover_pastas_vazias()

        # A pasta protegida em si não é removida
        assert (tmp_path / nome_protegido).exists()

    def test_pasta_vazia_apos_remocao_de_arquivo_e_removida(self, service, tmp_path, criar_arquivo, criar_pasta):
        """Se uma pasta fica vazia após remoção manual de arquivos antes da chamada,
        ela deve ser removida normalmente."""
        subpasta = criar_pasta(tmp_path, "ficou_vazia")
        arquivo = criar_arquivo(subpasta, "temp.txt")
        arquivo.unlink()  # remove o arquivo antes de chamar o serviço

        service.remover_pastas_vazias()

        assert not subpasta.exists()

    def test_pasta_com_subpasta_vazia_e_arquivo_nao_e_removida(self, service, tmp_path, criar_arquivo, criar_pasta):
        """Pasta que contém um arquivo e uma subpasta vazia não deve ser removida,
        apenas a subpasta interna vazia deve ser."""
        pai = criar_pasta(tmp_path, "pai")
        criar_arquivo(pai, "arquivo.txt")
        vazia_interna = criar_pasta(pai, "vazia_interna")

        service.remover_pastas_vazias()

        assert pai.exists()
        assert not vazia_interna.exists()