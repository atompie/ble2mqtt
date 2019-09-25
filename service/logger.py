import logging, os


class LoggerWrapper:

    def __init__(self, file=None):
        if file is not None and os.access(os.path.dirname(file), os.W_OK):
            logging.basicConfig(
                filename=file,
                format='%(asctime)s %(message)s', datefmt='[%m/%d/%Y %I:%M:%S %p]'
                , level=logging.DEBUG

            )
        else:
            logging.basicConfig(
                format='%(asctime)s %(message)s', datefmt='[%m/%d/%Y %I:%M:%S %p]'
                , level=logging.DEBUG
            )

    def info(self, text):
        logging.info(text)

    def debug(self, text):
        logging.debug(text)

    def warning(self, text):
        logging.warning(text)

    def error(self, text):
        logging.error(text)


if __name__ == '__main__':
    l = LoggerWrapper()
    l.info('text')
