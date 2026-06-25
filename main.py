import json
import os

from services.organizador import Organizador
from services.logger import configurar_logger
from services.database import DatabaseService

logger = configurar_logger()

PASTA_ALVO = r"C:\Users\samil\Downloads"
PROJETO_DIR = os.path.dirname(os.path.abspath(__file__)) 

db_path = os.path.join(PROJETO_DIR, "database", "organizador.db")
database = DatabaseService(logger=logger, caminho_db=db_path)

config_path = os.path.join(PROJETO_DIR, "config.json")

try:
    with open(config_path, "r", encoding="utf-8") as arquivo:
        regras = json.load(arquivo)
except FileNotFoundError:
    logger.error(f"Arquivo de configuração não encontrado: {config_path}")
    raise
except json.JSONDecodeError as erro:
    logger.error(f"config.json inválido: {erro}")
    raise

try:
    organizador = Organizador(pasta_alvo=PASTA_ALVO, regras=regras, logger=logger, database=database)

    organizador.processar()
except Exception as erro:
    logger.error(f"Falha na execução do organizador: {erro}")
    raise
finally:
    database.close()