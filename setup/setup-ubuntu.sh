#!/usr/bin/env bash

sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-dev
sudo apt-get install -y bluetooth libbluetooth-dev

sudo hciconfig hci0 up

pip3 install -r ../requirements.txt

sudo cp systemd/ble2mqtt.service /etc/systemd/system/ble2mqtt.service
sudo chown root:root /etc/systemd/system/ble2mqtt.service
sudo chmod 664 /etc/systemd/system/ble2mqtt.service

sudo systemctl daemon-reload

