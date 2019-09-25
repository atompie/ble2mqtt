from service.logger import LoggerWrapper


class MqttReporter:

    def __init__(self, server: str, port: int, credentials: tuple):
        self.user, self.password = credentials
        self.port = port
        self.server = server
        self.logger = LoggerWrapper()

    def enters(self, ble: dict) -> bool:
        self.logger.info("ble/scanner_name/ENTERS {}".format(ble))
        return True

    def leaves(self, ble: dict) -> bool:
        self.logger.info("ble/scanner_name/LEAVES {}".format(ble))
        return True

    def stays(self, ble: dict) -> bool:
        self.logger.info("ble/scanner_name/STAYS {}".format(ble))
        return True
