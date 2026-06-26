import os
import time

def gerar_caminho_unico(pasta_destino, nome_arquivo):
    destino = os.path.join(pasta_destino, nome_arquivo)
    
    if not os.path.exists(destino):
        return destino
    
    nome, extensao = os.path.splitext(nome_arquivo)
    novo_nome = f"{nome}_{int(time.time())}{extensao}"
    return os.path.join(pasta_destino, novo_nome)