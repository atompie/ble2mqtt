sudo hciconfig hci0 down
sleep 2
sudo hciconfig hci up
sudo python3 ble2mqtt "$@"
