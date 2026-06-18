import hashlib
import os


class HashService:

    @staticmethod
    def gerar_hash(caminho_arquivo):

        if not os.path.isfile(caminho_arquivo):
            raise ValueError(f"Não é um arquivo válido: {caminho_arquivo}" )

        sha256 = hashlib.sha256()

        with open(caminho_arquivo, "rb") as arquivo:

            while chunk := arquivo.read(4096):
                sha256.update(chunk)

        return sha256.hexdigest()