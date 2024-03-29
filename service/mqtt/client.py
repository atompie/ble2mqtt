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
        self.subscribe = subscribe

        client = mqtt_client.Client("ble2mqtt")
        client.on_connect = self._on_connect
        client.on_disconnect = self._on_disconnect

        client.loop_start()
        client.connected_flag = False
        client.username_pw_set(user, password=password)
        client.connect(server, port=port, keepalive=60)

        while not client.connected_flag:
            self.logger.info('Waiting for connection...')
            time.sleep(1)

        self.client = client

    def publish(self, topic, payload, qos=2):
        self.client.publish(topic, payload, qos)

    def subscribe(self, topic, callback, qos=2):
        self.client.on_message = callback
        self.client.subscribe(topic, qos)

    def disconnect(self):
        self.__del__()

    def __del__(self):
        self.client.loop_stop()
        self.client.disconnect()

    def _on_connect(self, client, userdata, flags, rc):
        if self.subscribe:
            client.on_message = self.subscribe.callback
            client.subscribe(self.subscribe.topic, self.subscribe.qos)

        self.logger.info("Connected with result code {}".format(rc))
        client.connected_flag = True

    def _on_disconnect(self, client, userdata, rc):
        self.logger.info("Client disconnected")
