import logging

from alarmer import Alarmer


class LoggingHandler(logging.Handler):
    def __init__(self, level: int = logging.ERROR):
        super().__init__()
        self.level = level

    def emit(self, record: logging.LogRecord) -> None:
        if record.levelno >= self.level:
            exc_info = record.exc_info
            exc = None
            if exc_info:
                exc = exc_info[1]
            Alarmer.send(record.getMessage(), exc)
