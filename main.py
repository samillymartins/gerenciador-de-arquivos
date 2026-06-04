import json

from services.organizador import Organizador
from services.logger import configurar_logger

logger = configurar_logger()
PASTA_ALVO = r"C:\Users\samil\Downloads"

with open("config.json", "r", encoding="utf-8") as arquivo:
    regras = json.load(arquivo)

organizador = Organizador(pasta_alvo=PASTA_ALVO, regras=regras, logger=logger)

organizador.organizar()