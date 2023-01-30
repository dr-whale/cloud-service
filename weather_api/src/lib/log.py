import logging
from config import config
from logging.handlers import RotatingFileHandler
from .class_description import Singleton


class Log (metaclass=Singleton):
    def __init__(self):
        self.level = config.LOGGER_LEVEL
        self.path = config.LOGGER_FILE_PATH
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(self.level)
        handler = RotatingFileHandler(filename=self.path, mode='a', maxBytes=8192, backupCount=5)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.propagate = False

    def __getattr__(self, name):
        if hasattr(self.logger, name):
            return getattr(self.logger, name)
        else:
            return getattr(self, name)