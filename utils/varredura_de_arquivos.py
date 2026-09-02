import os


def listar_arquivos(pasta_alvo, pastas_ignoradas=()):
    ignoradas = set(pastas_ignoradas)

    for raiz, diretorios, arquivos in os.walk(pasta_alvo):
        diretorios[:] = [d for d in diretorios if d not in ignoradas]

        for arquivo in arquivos:
            caminho = os.path.join(raiz, arquivo)
            if os.path.isfile(caminho):
                yield caminho
