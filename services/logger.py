import logging
import os


def configurar_logger():

    os.makedirs('logs', exist_ok=True)

    logging.basicConfig(
        filename='logs/log-organizacao.log',
        level=logging.INFO,
        encoding='utf-8',
        format='%(asctime)s | %(levelname)s | %(message)s'
    )


    return logging.getLogger()