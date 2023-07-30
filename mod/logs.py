import logging


class Logger:
    def __init__(self, filename: str = "app.log"):
        logging.basicConfig(
            filename=filename,
            filemode="w",
            level=logging.DEBUG,
        )
        self.logger = logging.getLogger()

    def debug(self, msg: str):
        self.logger.debug(msg)

    def error(self, msg: str):
        self.logger.error(msg)
