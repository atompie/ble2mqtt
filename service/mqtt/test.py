# def on_log(client, userdata, level, buf):
#     print("log: ", buf)


# client.on_log = on_log


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
# client.loop_start()

# def on_message(client, userdata, msg):
#     print(msg.topic + " " + str(msg.payload))
#
# sub = MqttSubscriber(topic= "ble/#", callback=on_message)
# # sub = None
# mqtt = MqttClient(
#     server="192.168.1.123",
#     user="risto", password="STrych12345",
#     logger=LoggerWrapper(),
#     subscribe=sub
# )
# mqtt.publish(topic="ble/name/ENTERS", payload="{asas1}")
# mqtt.publish(topic="ble/name/ENTERS", payload="{asas2}")
# mqtt.publish(topic="ble/name/ENTERS", payload="{asas3}")
# time.sleep(1)
# mqtt.disconnect()