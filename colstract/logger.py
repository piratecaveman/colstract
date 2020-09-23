import logging
import pathlib


class Logger(object):
    def __init__(self, name: str, log_file: str):
        self.log_file = log_file
        self.name = name

        if not pathlib.Path(self.log_file).parent.exists():
            pathlib.Path.mkdir(pathlib.Path(self.log_file).parent, parents=True)

        self.logger = logging.getLogger(self.name)
        handler = logging.FileHandler(filename=self.log_file, mode='w')
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(levelname)s]:%(name)s:%(asctime)s:%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def get_logger(self):
        return self.logger
