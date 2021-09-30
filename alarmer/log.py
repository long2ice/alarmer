import logging

from alarmer import Alarmer


class LoggingHandler(logging.Handler):
    def __init__(self, level: int = logging.ERROR):
        super().__init__()
        self.level = level

    def emit(self, record: logging.LogRecord) -> None:
        if record.levelno >= self.level:
            Alarmer.send(record.getMessage())
