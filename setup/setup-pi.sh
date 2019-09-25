#!/usr/bin/env bash

export LANGUAGE=en_GB.UTF-8
export LANG=en_GB.UTF-8
export LC_ALL=en_GB.UTF-8

sudo locale-gen en_GB.UTF-8
sudo dpkg-reconfigure locales

sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-dev
sudo apt-get install -y bluetooth libbluetooth-dev

pip3 install -r ../requirements.txt

sudo cp init.d/ble2mqtt /etc/init.d/ble2mqtt
sudo chown root:root /etc/init.d/ble2mqtt
sudo chmod 755 /etc/init.d/ble2mqtt

sudo systemctl daemon-reload

