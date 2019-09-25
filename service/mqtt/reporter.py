import json
from service.logger import LoggerWrapper
from service.mqtt.client import MqttSubscriber, MqttClient


class MqttReporter:

    def __init__(self, scanner_name: str, server: str, port: int, credentials: tuple, logger: LoggerWrapper):
        user, password = credentials
        self.logger = logger

        self.mqtt_client = MqttClient(
            server=server, user=user, password=password, port=port,
            logger=logger,
            subscribe=MqttSubscriber(topic="ble/{}/CMND".format(scanner_name), callback=self._on_cmnd)
        )

        self.topic = "ble/{}".format(scanner_name)

    def _on_cmnd(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))

    def enters(self, ble: dict):
        self.logger.debug("ble/scanner_name/ENTERS {}".format(ble))
        return self.mqtt_client.publish(
            topic="{}/ENTERS".format(self.topic),
            payload=json.dumps(ble))

    def leaves(self, ble: dict):
        self.logger.debug("ble/scanner_name/LEAVES {}".format(ble))
        return self.mqtt_client.publish(
            topic="{}/LEAVES".format(self.topic),
            payload=json.dumps(ble))

    def stays(self, ble: dict):
        self.logger.debug("ble/scanner_name/STAYS {}".format(ble))
        return self.mqtt_client.publish(
            topic="{}/STAYS".format(self.topic),
            payload=json.dumps(ble),
            qos=0)
