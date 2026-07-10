import os
import pytest
from utils.gerador_de_caminho_unico import gerar_caminho_unico


class TestGerarCaminhoUnico:

    def test_retorna_caminho_original_se_nao_existe(self, tmp_path):
        """quando o arquivo não existe no destino, retorna o caminho sem alteração."""
        resultado = gerar_caminho_unico(tmp_path, "arquivo.txt")

        assert resultado == os.path.join(tmp_path, "arquivo.txt")

    def test_gera_nome_diferente_se_arquivo_ja_existe(self, tmp_path):
        """quando já existe um arquivo com o mesmo nome, retorna um caminho diferente."""
        (tmp_path / "arquivo.txt").write_text("conteudo")

        resultado = gerar_caminho_unico(tmp_path, "arquivo.txt")

        assert resultado != os.path.join(tmp_path, "arquivo.txt")

    def test_preserva_extensao_no_nome_unico(self, tmp_path):
        """o nome gerado para evitar colisão deve preservar a extensão original."""
        (tmp_path / "arquivo.txt").write_text("conteudo")

        resultado = gerar_caminho_unico(tmp_path, "arquivo.txt")

        assert resultado.endswith(".txt")

    def test_preserva_pasta_destino_no_nome_unico(self, tmp_path):
        """o caminho gerado deve apontar para a mesma pasta de destino."""
        (tmp_path / "arquivo.txt").write_text("conteudo")

        resultado = gerar_caminho_unico(tmp_path, "arquivo.txt")

        assert os.path.dirname(resultado) == str(tmp_path)

    def test_funciona_com_extensao_dupla(self, tmp_path):
        """preserva apenas a última extensão em arquivos com extensão dupla."""
        (tmp_path / "arquivo.tar.gz").write_text("conteudo")

        resultado = gerar_caminho_unico(tmp_path, "arquivo.tar.gz")

        assert resultado.endswith(".gz")

    def test_caminho_unico_nao_colide_com_existente(self, tmp_path):
        """o caminho retornado não deve apontar para um arquivo que já existe."""
        (tmp_path / "arquivo.txt").write_text("conteudo")

        resultado = gerar_caminho_unico(tmp_path, "arquivo.txt")

        assert not os.path.exists(resultado)