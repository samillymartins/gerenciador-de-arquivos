import os
import shutil
import time
from datetime import datetime

from services.duplicate_service import DuplicateService
from utils.gerador_de_caminho_unico import gerar_caminho_unico
from core.constants import PASTA_DUPLICADOS
from services.cleanup_services import CleanupService

class Organizador:
    def __init__(self, pasta_alvo, regras, logger, database):
        self.pasta_alvo = pasta_alvo
        self.regras = regras
        self.logger = logger
        self.database = database
        
        self.duplicate_service = DuplicateService(pasta_alvo, logger)
        self.cleanup_service = CleanupService(pasta_alvo, logger)
        
        self.mapa_extensoes = {}
        for pasta, extensoes in regras.items():
            for extensao in extensoes:
                self.mapa_extensoes[extensao.lower()] = pasta
        
        self.processados = 0
        self.movidos = 0
        self.ignorados = 0
        self.erros = 0
        self.estatisticas = {}

    def exibir_resumo(self, tempo_total):

        resumo = f"""
        ================================
        RESUMO DA EXECUÇÃO
        ================================

        Arquivos processados: {self.processados}
        Arquivos movidos: {self.movidos}
        Ignorados: {self.ignorados}
        Erros: {self.erros}
        Duplicados encontrados: {self.duplicate_service.duplicados_encontrados}

        Tempo total: {tempo_total}s
        ================================
        """

        resumo += "\nArquivos por categoria:\n"

        for categoria, quantidade in self.estatisticas.items():
            resumo += f"{categoria}: {quantidade}\n"

        self.logger.info(resumo)
        
    def listar_arquivos(self):
        pastas_ignoradas = set(self.regras.keys())
        pastas_ignoradas.add(PASTA_DUPLICADOS)
        
        for raiz, diretorios, arquivos in os.walk(self.pasta_alvo):
            diretorios[:] = [d for d in diretorios if d not in pastas_ignoradas]

            for arquivo in arquivos:
                yield os.path.join(raiz, arquivo)

    def organizar(self):
        movimentacoes_db = []
        inicio = time.time()
        
        for arquivo in self.listar_arquivos():
            if not os.path.isfile(arquivo):
                continue
            
            self.processados += 1
            nome_arquivo = os.path.basename(arquivo)
            _, extensao = os.path.splitext(arquivo)
            
            pasta = self.mapa_extensoes.get(extensao.lower())
            
            if not pasta:
                self.ignorados += 1
                self.logger.warning(f"Extensão não mapeada: {nome_arquivo}.")
                continue
            
            pasta_origem = os.path.dirname(arquivo)
            destino_pasta = os.path.join(pasta_origem, pasta)
            
            try: 
                os.makedirs(destino_pasta, exist_ok=True)
                
                destino = gerar_caminho_unico(destino_pasta, nome_arquivo)
                shutil.move(arquivo, destino)
                self.movidos += 1
                self.estatisticas[pasta] = self.estatisticas.get(pasta, 0) + 1
                        
                movimentacoes_db.append((nome_arquivo, extensao, pasta, self.pasta_alvo, destino, datetime.now().isoformat()))
                self.logger.info(f"Movendo '{nome_arquivo}' para '{destino}'.")
                        
            except Exception as erro:
                self.logger.error(f"Erro ao mover '{nome_arquivo}': {erro}")
                self.erros += 1

        if movimentacoes_db:
            if hasattr(self.database, 'salvar_movimentacoes_em_lote'):
                    self.database.salvar_movimentacoes_em_lote(movimentacoes_db)
            else:
                    for movimentacao in movimentacoes_db:
                        self.database.salvar_movimentacao(*movimentacao)

        fim = time.time()
        tempo_total = round(fim - inicio, 2)
        self.exibir_resumo(tempo_total)
        self.logger.info("Organização concluída!")

    def gerar_relatorio(self):
        self.database.gerar_relatorio()
        
    def processar(self):
        self.duplicate_service.encontrar_duplicados()
        self.duplicate_service.mover_para_duplicados()
        self.organizar()
        self.cleanup_service.remover_pastas_vazias()
        self.gerar_relatorio()