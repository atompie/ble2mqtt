# Welcome

I just released a library to scan Bluetooth Low Engine devices for Smart Home fans.

It scans bluetooth devices and sends data about the appearance of a bluetooth device to the defined MQTT server. The software works great on the Raspberry Pi so you can get a few bluetooth scanners.

I used this solution to report the presence of household members. It works great with the node-red server.

Show me that you like this project and star it ande enjoy. 

# ble2mqtt

Ble2mqtt service is a simple BLE scanner that publishes information to mqtt server when new BLE device enters or leaves the scanner discovery range.

# Requirements

    sudo apt-get update
    sudo apt-get install -y python3 python3-pip python3-dev
    sudo apt-get install -y bluetooth libbluetooth-dev

    sudo systemctl unmask bluetooth
    sudo systemctl enable bluetooth
    sudo systemctl start bluetooth
    
### Install bluez
#### Ubuntu
    sudo apt-get install -y libudev-dev libical-dev libreadline6-dev libdbus-1-dev libglib2.0-dev
#### Rasberry pi
    sudo apt-get install -y libusb-dev libdbus-1-dev libglib2.0-dev libudev-dev libical-dev libreadline-dev

```    
wget http://www.kernel.org/pub/linux/bluetooth/bluez-5.49.tar.xz
tar xvf bluez-5.49.tar.xz
./configure
make
sudo make install
```

# Installation

    cd /opt
    git clone https://github.com/atompie/ble2mqtt.git
    cd ble2mqtt
    pip install -r requirements.txt
    sudo chmod 755 ble2mqtt
    sudo chmod 755 ble2mqtt.sh

## Service installation 

Service installation depends on the system type you are installting the service. 
If you are running rasberry PI please edit file in init.d/ble2mqtt. Find line with <set_name>, <set_server>
and fill it with your settings.

Do the same for Ubuntu installation but in file systemd/ble2mqtt.service

### Ubuntu service installation

    sudo bash setup/setup-ubuntu.sh

### Raspberry PI service installation

    sudo bash setup/setup-ubuntu.sh
    
## Test manually

    sudo ble2mqtt --server 192.168.1.100 --name Livingroom
    
## Start service

    sudo service ble2mqtt start
    
## Auto start service 

    sudo systemctl enable ble2mqtt
    
# Mqtt topics

todo
