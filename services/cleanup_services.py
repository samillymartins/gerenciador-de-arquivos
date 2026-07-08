import os
from core.constants import PASTAS_PROTEGIDAS


class CleanupService:

    def __init__(self, pasta_alvo, logger):
        self.pasta_alvo = pasta_alvo
        self.logger = logger
        

    def remover_pastas_vazias(self):
        for raiz, diretorios, arquivos in os.walk( self.pasta_alvo, topdown=False):
            if os.path.basename(raiz) in PASTAS_PROTEGIDAS:
                continue
            if raiz == self.pasta_alvo:
                continue

            try:
                if not os.listdir(raiz):
                    os.rmdir(raiz)
                    self.logger.info(f"Pasta vazia removida: {raiz}")

            except Exception as erro:
                self.logger.error(f"Erro ao remover '{raiz}': {erro}")