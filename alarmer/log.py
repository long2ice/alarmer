import logging

from alarmer import Alarmer


class LoggingHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        if record.levelno >= logging.ERROR:
            Alarmer.send(record.getMessage())
