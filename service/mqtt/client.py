import paho.mqtt.client as mqtt_client
import time


class MqttSubscriber:
    def __init__(self, topic, callback, qos=2):
        self.qos = qos
        self.callback = callback
        self.topic = topic


class MqttClient:

    def __init__(self, server, user, logger, port=1883, password=None, subscribe: MqttSubscriber = None):

        self.logger = logger

        client = mqtt_client.Client("ble2mqtt")
        client.on_connect = self._on_connect
        client.on_publish = self._on_publish
        client.on_disconnect = self._on_disconnect
        if subscribe:
            client.on_message = subscribe.callback

        client.loop_start()
        client.connected_flag = False
        client.username_pw_set(user, password=password)
        client.connect(server, port=port, keepalive=60)

        while not client.connected_flag:
            self.logger.info('Waiting for connection...')
            time.sleep(1)

        if subscribe:
            client.subscribe(subscribe.topic, subscribe.qos)

        self.client = client

    def publish(self, topic, payload, qos=2):
        print(self.client.publish(topic, payload, qos))

    def subscribe(self, topic, callback, qos=2):
        self.client.on_message = callback
        self.client.subscribe(topic, qos)

    def disconnect(self):
        self.__del__()

    def __del__(self):
        self.client.loop_stop()
        self.client.disconnect()

    def _on_connect(self, client, userdata, flags, rc):
        self.logger.info("Connected with result code {}".format(rc))
        client.connected_flag = True

    def _on_disconnect(self, client, userdata, rc):
        self.logger.info("Client disconnected")

    def _on_publish(self, client, userdata, result):
        self.logger.info("Data published with id {}".format(result))

