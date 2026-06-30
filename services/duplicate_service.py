import os
import shutil
import time

from core.constants import PASTA_DUPLICADOS
from services.hash_service import HashService
from utils.gerador_de_caminho_unico import gerar_caminho_unico

class DuplicateService:

    def __init__(self, pasta_alvo, logger):
        self.pasta_alvo = pasta_alvo
        self.logger = logger
        
        self.duplicados_encontrados = 0
        self.duplicados_movidos = 0
        self._ultimos_duplicados = []
        
    def _listar_arquivos(self):
        for raiz, diretorios, arquivos in os.walk(self.pasta_alvo):
            diretorios = [d for d in diretorios if d != PASTA_DUPLICADOS]
            for arquivo in arquivos:
                caminho = os.path.join(raiz, arquivo)
                if os.path.isfile(caminho):
                    yield caminho
    
    def encontrar_duplicados(self):
        arquivos_por_tamanho = {}
        
        for caminho in self._listar_arquivos():
            try:
                tamanho = os.path.getsize(caminho)
            except OSError as erro:
                self.logger.error(f"Erro ao obter acessar o '{caminho}': {erro}")
                continue
            arquivos_por_tamanho.setdefault(tamanho, []).append(caminho)
            
        hashes = {}
        duplicados = []

        for tamanho, arquivos in arquivos_por_tamanho.items():
            if len(arquivos) < 2:
                continue
            for arquivo in arquivos:      
                try:
                    hash_arquivo = (HashService.gerar_hash(arquivo))
                    self.logger.info(f"Gerando hash para '{arquivo}': {hash_arquivo}")

                    if hash_arquivo in hashes:
                        duplicados.append({
                            "original": hashes[hash_arquivo],
                            "duplicado": arquivo,
                            "hash": hash_arquivo,
                            "tamanho": tamanho})
                        self.logger.warning(f"Arquivo duplicado encontrado: {arquivo} (hash: {hash_arquivo})")
                        continue
                    
                    hashes[hash_arquivo] = arquivo
                        
                except Exception as erro:
                    self.logger.error(f"Erro ao gerar hash de "f"{arquivo}: {erro}")
                    continue
                
        self.duplicados_encontrados = len(duplicados)
        self._ultimos_duplicados = duplicados
        return duplicados
    
    def mover_para_duplicados(self, duplicados=None):
        duplicados = duplicados if duplicados is not None else self._ultimos_duplicados

        pasta_duplicados = os.path.join(self.pasta_alvo, PASTA_DUPLICADOS)
            
        os.makedirs(pasta_duplicados, exist_ok=True)
        
        for info in duplicados:
            caminho_origem = info["duplicado"]
            nome_arquivo = os.path.basename(caminho_origem)
            destino = gerar_caminho_unico(pasta_duplicados, nome_arquivo)
            
            try:
                shutil.move(caminho_origem,destino)
                self.duplicados_movidos += 1

                self.logger.warning(f"Arquivo duplicado movido para Duplicados: {nome_arquivo}")
            except Exception as erro:
                self.logger.error(f"Erro ao mover arquivo duplicado '{nome_arquivo}': {erro}")
        
    def exibir_duplicados(self):
        duplicados = self._ultimos_duplicados

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