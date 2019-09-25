import json
from service.logger import LoggerWrapper
from service.mqtt.client import MqttSubscriber, MqttClient


class MqttReporter:

    def __init__(self, scanner_name: str, server: str, port: int, credentials: tuple, logger: LoggerWrapper):
        user, password = credentials
        self._logger = logger
        self._topic = "ble/{}".format(scanner_name)
        self._mqtt_client = MqttClient(
            server=server, user=user, password=password, port=port,
            logger=logger,
            subscribe=MqttSubscriber(topic="{}/CMND".format(self._topic), callback=self._on_cmnd)
        )

        self._scanner_name = scanner_name
        self.require_update = False

    def _on_cmnd(self, client, userdata, msg):
        if msg.payload.lower() == b'update':
            self.require_update = True
            self._logger.info("{}/CMND {}".format(self._topic, msg.payload))

    def enters(self, ble: dict):
        self._logger.debug("{}/ENTERS {}".format(self._topic, ble))
        return self._mqtt_client.publish(
            topic="{}/ENTERS".format(self._topic),
            payload=json.dumps(ble))

    def leaves(self, ble: dict):
        self._logger.debug("{}/LEAVES {}".format(self._topic, ble))
        return self._mqtt_client.publish(
            topic="{}/LEAVES".format(self._topic),
            payload=json.dumps(ble))

    def update(self, ble: dict):
        self._logger.debug("{}/UPDATE {}".format(self._topic, ble))
        return self._mqtt_client.publish(
            topic="{}/UPDATE".format(self._topic),
            payload=json.dumps(ble),
            qos=0)
