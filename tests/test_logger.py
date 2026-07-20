import logging
import os
import pytest
from logging.handlers import TimedRotatingFileHandler
from unittest.mock import patch


@pytest.fixture(autouse=True)
def resetar_logger():
    """
    Remove handlers e reseta o logger "organizador" antes de cada teste.
    Sem isso, o estado do logger vaza entre testes — já que o logging
    do Python mantém loggers em memória durante toda a sessão do pytest.
    """
    logger = logging.getLogger("organizador")
    logger.handlers.clear()
    logger.propagate = True
    yield
    logger.handlers.clear()
    logger.propagate = True


@pytest.fixture
def pasta_logs(tmp_path, monkeypatch):
    """
    Redireciona a criação da pasta de logs para tmp_path, evitando
    criar a pasta 'logs/' real durante os testes.
    """
    monkeypatch.chdir(tmp_path)
    return tmp_path / "logs"


class TestConfigurarLogger:

    def test_retorna_logger_nomeado(self, pasta_logs):
        """Deve retornar o logger com o nome 'organizador'."""
        from services.logger import configurar_logger

        logger = configurar_logger()

        assert logger.name == "organizador"

    def test_nivel_info(self, pasta_logs):
        """O logger deve estar configurado com nível INFO."""
        from services.logger import configurar_logger

        logger = configurar_logger()

        assert logger.level == logging.INFO

    def test_cria_pasta_logs(self, pasta_logs):
        """A pasta 'logs/' deve ser criada se não existir."""
        from services.logger import configurar_logger

        configurar_logger()

        assert pasta_logs.exists()

    def test_adiciona_timed_rotating_handler(self, pasta_logs):
        """Deve adicionar exatamente um TimedRotatingFileHandler."""
        from services.logger import configurar_logger

        logger = configurar_logger()

        handlers = [h for h in logger.handlers if isinstance(h, TimedRotatingFileHandler)]
        assert len(handlers) == 1

    def test_handler_rotaciona_a_meia_noite(self, pasta_logs):
        """O handler deve estar configurado para rotacionar à meia-noite."""
        from services.logger import configurar_logger

        logger = configurar_logger()

        handler = logger.handlers[0]
        assert handler.when == "MIDNIGHT"

    def test_handler_mantem_30_backups(self, pasta_logs):
        """O handler deve manter 30 arquivos de backup."""
        from services.logger import configurar_logger

        logger = configurar_logger()

        handler = logger.handlers[0]
        assert handler.backupCount == 30

    def test_handler_usa_encoding_utf8(self, pasta_logs):
        """O handler deve usar encoding UTF-8."""
        from services.logger import configurar_logger

        logger = configurar_logger()

        handler = logger.handlers[0]
        assert handler.encoding == "utf-8"

    def test_formato_da_mensagem(self, pasta_logs):
        """O formatter deve seguir o padrão 'data | nível | mensagem'."""
        from services.logger import configurar_logger

        logger = configurar_logger()

        formatter = logger.handlers[0].formatter
        assert formatter._fmt == "%(asctime)s | %(levelname)s | %(message)s"

    def test_propagate_false(self, pasta_logs):
        """propagate deve ser False para não poluir o root logger."""
        from services.logger import configurar_logger

        logger = configurar_logger()

        assert logger.propagate is False

    def test_nao_duplica_handlers_em_chamadas_multiplas(self, pasta_logs):
        """Chamadas repetidas a configurar_logger() não devem duplicar handlers."""
        from services.logger import configurar_logger

        configurar_logger()
        configurar_logger()
        configurar_logger()

        logger = logging.getLogger("organizador")
        assert len(logger.handlers) == 1

    def test_arquivo_de_log_criado_no_caminho_correto(self, pasta_logs):
        """O arquivo de log deve ser criado dentro da pasta 'logs/'."""
        from services.logger import configurar_logger

        logger = configurar_logger()
        logger.info("mensagem de teste")

        handler = logger.handlers[0]
        assert os.path.dirname(handler.baseFilename).endswith("logs")