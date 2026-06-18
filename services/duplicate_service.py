import os
import shutil
import time

from services.hash_service import HashService

class DuplicateService:

    def __init__(self, pasta_alvo, logger):
        self.pasta_alvo = pasta_alvo
        self.logger = logger
        
    def encontrar_duplicados(self):
        hashes = {}
        duplicados = []

        for arquivo in os.listdir(self.pasta_alvo):
                caminho_arquivo = os.path.join(self.pasta_alvo, arquivo)
                
                if not os.path.isfile(caminho_arquivo):
                    continue
                try:
                    hash_arquivo = (HashService.gerar_hash(caminho_arquivo))
                    self.logger.info(f"Gerando hash para '{arquivo}': {hash_arquivo}")

                    if hash_arquivo in hashes:
                        duplicados.append({
                            "original": hashes[hash_arquivo],
                            "duplicado": arquivo,
                            "hash": hash_arquivo,
                            "tamanho": os.path.getsize(caminho_arquivo)})
                        self.mover_para_duplicados(caminho_arquivo, arquivo)
                        self.logger.warning(f"Arquivo duplicado encontrado: {arquivo} (hash: {hash_arquivo})")
                      
                        continue
                    
                    hashes[hash_arquivo] = arquivo
                        
                except Exception as erro:
                    self.logger.error(f"Erro ao gerar hash de "f"{arquivo}: {erro}")
                    
                    continue

        return duplicados
    
    def mover_para_duplicados(self, caminho_arquivo, arquivo):
        pasta_duplicados = os.path.join(self.pasta_alvo, "Duplicados")
            
        os.makedirs(pasta_duplicados, exist_ok=True)
        destino = os.path.join(pasta_duplicados, arquivo)
            
        if os.path.exists(destino):
            nome, extensao = os.path.splitext(arquivo)
            destino = os.path.join(pasta_duplicados, f"{nome}_{int(time.time())}{extensao}")

        shutil.move(caminho_arquivo,destino)
        self.movidos += 1

        self.logger.warning(f"Arquivo duplicado movido para Duplicados: {arquivo}")
        
    def exibir_duplicados(self):
        duplicados = (self.encontrar_duplicados())

        if not duplicados:
            self.logger.info("\nNenhum arquivo duplicado encontrado.")
            return
        
        self.logger.info("\nArquivos duplicados encontrados:\n")

        for duplicado_info in duplicados:
            self.logger.info(f"Original: {duplicado_info['original']}")
            self.logger.info(f"Duplicado: {duplicado_info['duplicado']}")
            self.logger.info(f"Hash: {duplicado_info['hash']}")
            self.logger.info(f"Tamanho: {duplicado_info['tamanho']} bytes")
            self.logger.info("-" * 40)