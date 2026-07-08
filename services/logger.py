import logging
import os
from logging.handlers import TimedRotatingFileHandler


def configurar_logger():

    os.makedirs('logs', exist_ok=True)
    
    logger = logging.getLogger("organizador")
    logger.setLevel(logging.INFO)
    
    if logger.handlers:
        return logger
    
    handler = TimedRotatingFileHandler(
        filename='logs/log-organizacao.log',
        when='midnight',
        interval=1,
        backupCount=30,
        encoding='utf-8'
    )
    
    handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
    
    logger.addHandler(handler)
    logger.propagate = False
    
    return logger
