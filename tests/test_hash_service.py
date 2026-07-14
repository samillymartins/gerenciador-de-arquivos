import pytest
from services.hash_service import HashService

class TestHashService:

    def test_gera_hash_de_arquivo_valido(self, tmp_path):
        """deve retornar uma string hexadecimal para um arquivo válido."""
        arquivo = tmp_path / "arquivo.txt"
        arquivo.write_text("conteudo")

        resultado = HashService.gerar_hash(str(arquivo))

        assert isinstance(resultado, str)
        assert len(resultado) == 64  
        
    def test_hash_identico_para_mesmo_conteudo(self, tmp_path):
        """dois arquivos com o mesmo conteúdo devem gerar o mesmo hash."""
        arquivo_a = tmp_path / "a.txt"
        arquivo_b = tmp_path / "b.txt"
        arquivo_a.write_text("conteudo igual")
        arquivo_b.write_text("conteudo igual")

        assert HashService.gerar_hash(str(arquivo_a)) == HashService.gerar_hash(str(arquivo_b))

    def test_hash_diferente_para_conteudos_distintos(self, tmp_path):
        """arquivos com conteúdos diferentes devem gerar hashes diferentes."""
        arquivo_a = tmp_path / "a.txt"
        arquivo_b = tmp_path / "b.txt"
        arquivo_a.write_text("conteudo A")
        arquivo_b.write_text("conteudo B")

        assert HashService.gerar_hash(str(arquivo_a)) != HashService.gerar_hash(str(arquivo_b))

    def test_gera_hash_de_arquivo_vazio(self, tmp_path):
        """deve gerar hash mesmo para arquivo vazio, sem lançar exceção."""
        arquivo = tmp_path / "vazio.txt"
        arquivo.write_text("")

        resultado = HashService.gerar_hash(str(arquivo))

        assert isinstance(resultado, str)
        assert len(resultado) == 64

    def test_lanca_erro_para_caminho_inexistente(self, tmp_path):
        """deve lançar ValueError para um caminho que não existe."""
        caminho_invalido = str(tmp_path / "nao_existe.txt")

        with pytest.raises(ValueError):
            HashService.gerar_hash(caminho_invalido)

    def test_lanca_erro_para_diretorio(self, tmp_path):
        """deve lançar ValueError quando o caminho aponta para um diretório."""
        with pytest.raises(ValueError):
            HashService.gerar_hash(str(tmp_path))