import logging
import sys


class Logger:
    _logger = None
    def __init__(self):
        Logger._logger = logging.getLogger("logger")
        handler = logging.StreamHandler(stream=sys.stdout)
        Logger._logger.addHandler(handler)

    @staticmethod
    def get_logger(cls):
        if Logger._logger is None:
            return cls()

        return Logger._logger
