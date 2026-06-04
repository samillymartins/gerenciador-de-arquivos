import os
import shutil
import time

class Organizador:
    def __init__(self, pasta_alvo, regras, logger):
        self.pasta_alvo = pasta_alvo
        self.regras = regras
        self.logger = logger

    def exibir_resumo(self, tempo_total):

        resumo = f"""
        ================================
        RESUMO DA EXECUÇÃO
        ================================

        Arquivos processados: {self.processados}
        Arquivos movidos: {self.movidos}
        Ignorados: {self.ignorados}
        Erros: {self.erros}

        Tempo total: {tempo_total}s
        ================================
        """

        resumo += "\nArquivos por categoria:\n"

        for categoria, quantidade in self.estatisticas.items():
            resumo += f"{categoria}: {quantidade}\n"


        print(resumo)

        self.logger.info(resumo)

    def organizar(self):
        self.processados = 0
        self.movidos = 0
        self.ignorados = 0
        self.erros = 0

        self.estatisticas = {}

        inicio = time.time()
        for arquivo in os.listdir(self.pasta_alvo):

            caminho_arquivo = os.path.join(self.pasta_alvo, arquivo)

            if not os.path.isfile(caminho_arquivo):
                continue

            _, extensao = os.path.splitext(arquivo)
            self.processados += 1
            movido = False
            
            for pasta, extensoes in self.regras.items():
                
                if extensao.lower() in extensoes:
                    destino = os.path.join(self.pasta_alvo, pasta)
            
                    os.makedirs(destino, exist_ok=True)
                    try: 
                        shutil.move(caminho_arquivo, destino)
                        self.movidos += 1
                        self.estatisticas[pasta] = self.estatisticas.get(pasta, 0) + 1
                        self.logger.info(f"Movendo '{arquivo}' para '{destino}'.")
                        movido = True
                        break
                    except Exception as erro:
                        self.logger.error(f"Erro ao mover '{arquivo}': {erro}")
                        self.erros += 1

            if not movido:
                self.ignorados += 1
                self.logger.warning(f"Extensão não mapeada: \n{arquivo}.")

        fim = time.time()
        tempo_total = round(fim - inicio, 2)

        self.exibir_resumo(tempo_total)

        self.logger.info("Organização concluída!")
