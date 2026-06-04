import os
import shutil

class Organizador:
    def __init__(self, pasta_alvo, regras):
        self.pasta_alvo = pasta_alvo
        self.regras = regras

    def organizar(self):
        for arquivo in os.listdir(self.pasta_alvo):

            caminho_arquivo = os.path.join(self.pasta_alvo, arquivo)

            if not os.path.isfile(caminho_arquivo):
                continue

            _, extensao = os.path.splitext(arquivo)
            
            for pasta, extensoes in self.regras.items():
                
                if extensao.lower() in extensoes:
                    destino = os.path.join(self.pasta_alvo, pasta)
            
                    os.makedirs(destino, exist_ok=True)

                    shutil.move(caminho_arquivo, destino)
                    print(f"Movendo '{arquivo}' para '{destino}'")
                    break

        print("Organização concluída!")
