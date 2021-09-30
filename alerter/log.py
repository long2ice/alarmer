import logging

from alerter import Alerter


class LoggingHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        if record.levelno >= logging.ERROR:
            Alerter.send(record.getMessage())
