import sys
import os
import struct
from ctypes import (CDLL, get_errno)
from ctypes.util import find_library
import socket
from socket import (
    AF_BLUETOOTH,
    SOCK_RAW,
    BTPROTO_HCI,
    SOL_HCI,
    HCI_FILTER,
)
import errno
from time import time
from service.logger import LoggerWrapper


class BleScanner:

    def __init__(self, reporter, scanner_name: str, logger: LoggerWrapper, timeout: int = 12,
                 remove_after_sec: int = 90, throttle_mqtt_stay_publish: int = 60):

        self.postpone_logging = dict()
        self.time_mark = dict()
        self.remove_after_sec = remove_after_sec
        self.scanner_name = scanner_name
        self.timeout = timeout
        self.ble_devices = dict()
        self.logger = logger
        self.reporter = reporter
        self.discovery_counter = dict()
        self.throttle_mqtt_stay_publish = throttle_mqtt_stay_publish
        self.ble_devices = dict()

        if not os.geteuid() == 0:
            self.logger.error("Service ble2mqtt works as root only.")
            sys.exit("Run as root")

        bluetooth_lib = find_library("bluetooth")
        if not bluetooth_lib:
            raise Exception(
                "Can't find required bluetooth libraries"
                " (need to install bluez)"
            )

        bluez = CDLL(bluetooth_lib, use_errno=True)

        dev_id = bluez.hci_get_route(None)

        self.sock = socket.socket(AF_BLUETOOTH, SOCK_RAW, BTPROTO_HCI)
        self.sock.bind((dev_id,))

        err = bluez.hci_le_set_scan_parameters(self.sock.fileno(), 0, 0x10, 0x10, 0, 0, 1000)
        if err < 0:
            raise Exception("Set scan parameters failed")
            # occurs when scanning is still enabled from previous call

        # allows LE advertising events
        hci_filter = struct.pack(
            "<IQH",
            0x00000010,
            0x4000000000000000,
            0
        )
        self.sock.setsockopt(SOL_HCI, HCI_FILTER, hci_filter)
        self.sock.settimeout(timeout)

        err = bluez.hci_le_set_scan_enable(
            self.sock.fileno(),
            1,  # 1 - turn on;  0 - turn off
            0,  # 0-filtering disabled, 1-filter out duplicates
            1000  # timeout
        )
        if err < 0:
            errnum = get_errno()
            raise Exception("{} {}".format(
                errno.errorcode[errnum],
                os.strerror(errnum)
            ))

    def _discover(self, data):

        if data:

            # print bluetooth address from LE Advert. packet
            mac = ':'.join("{0:02x}".format(x) for x in data[12:6:-1])
            unsigned = data[-1]
            rssi = unsigned - 256 if unsigned > 127 else unsigned
            timestamp = int(time())

            if mac not in self.discovery_counter:
                self.discovery_counter[mac] = 0
            else:
                self.discovery_counter[mac] += 1

            ble = {
                'scanner': self.scanner_name,
                'mac': mac,
                'rssi': rssi,
                'timestamp': timestamp
            }

            # ble gets removed from ble_devices in collector
            # every 5 minutes if not discovered

            if mac not in self.ble_devices:

                # Device enters into scanner discovery range
                self.reporter.enters(ble)
                self.logger.info("\033[30;43m[ENTERS]\033[0m %s %s / %d" % (
                    mac, rssi, self.discovery_counter[mac]))

            else:

                if mac not in self.postpone_logging:
                    self.postpone_logging[mac] = timestamp
                elif self.postpone_logging[mac] + self.throttle_mqtt_stay_publish < timestamp:
                    self.postpone_logging[mac] = timestamp
                    # Device stays in scanner discovery range
                    self.reporter.stays(ble)
                    self.logger.info("\033[0;33m[STAYS]\033[0m %s %s / %d" % (
                        mac, rssi, self.discovery_counter[mac]))
                    self.discovery_counter[mac] = 0

            self.ble_devices[mac] = ble

    def _purge(self):
        """
        Removes device if it has not been discovered for some time (self.remove_after_sec).
        Purge is performed every 60 sec.
        """

        if self._time_passed('for_ble_delete', 30):  # Check if to clear every 30 sec

            """
            Removes device after some time if not discovered
            """

            for mac, ble in list(self.ble_devices.items()):
                if ble['timestamp'] + self.remove_after_sec < int(time()):
                    # Device leaves scanner discovery range
                    self.reporter.leaves(ble)
                    del self.ble_devices[mac]
                    if mac in self.postpone_logging:
                        del self.postpone_logging[mac]
                    if mac in self.discovery_counter:
                        del self.discovery_counter[mac]

                    self.logger.info("\033[0;31m[LEAVES]\033[0m %s removed from BLE devices" % mac)

    def _time_passed(self, name, delay):
        now = int(time())
        if name not in self.time_mark:
            self.time_mark[name] = now
        if now > self.time_mark[name] + delay:  # Clean after x sec
            self.time_mark[name] = now
            return True
        return False

    def scan(self):

        while True:

            try:

                data = self.sock.recv(1024)
                self._discover(data)

            except socket.timeout:
                self.logger.info("[TIMEOUT] No BLE device discovered in %s sec" % str(self.timeout))
            except OSError as e:
                print("\033[0;31m[ERR]\033[0m " + str(e))

            self._purge()
