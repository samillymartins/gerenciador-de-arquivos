import json

from services.organizador import Organizador


PASTA_ALVO = r"C:\Users\samil\Downloads"

with open("config.json", "r", encoding="utf-8") as arquivo:
    regras = json.load(arquivo)

organizador = Organizador(pasta_alvo=PASTA_ALVO, regras=regras)

organizador.organizar()