from service.ble_scanner import BleScanner
import argparse
from service.logger import LoggerWrapper
from service.mqtt_reporter import MqttReporter

"""
    Scans for new BLE devices. Reports it to server immediately if new devices is discovered
    or after a delay if device leaves scanner range.
"""

parser = argparse.ArgumentParser()
parser.add_argument("--name", help="Scanner name", required=True)
parser.add_argument("--server", help="Central server ip address", required=True)
parser.add_argument("--port", help="Server port", default=1883, type=int)
parser.add_argument("--user", help="Username")
parser.add_argument("--password", help="Password")
parser.add_argument("--timeout", help="Server timeout in seconds", default=5, type=int)
parser.add_argument("--send-every", help="Send data to server every sec", default=60, type=int)
parser.add_argument("--log", help="Log to file")
parser.add_argument("--error-log", help="Log errors to file")

args = parser.parse_args()

mqtt = MqttReporter(server=args.server, port=args.port, credentials=(args.user, args.password))
logger = LoggerWrapper(file=args.log)

# Scans bluetooth for ble devices
try:
    scanner = BleScanner(
        reporter=mqtt,  # used for immediate reporting of new ble devices
        scanner_name=args.name,
        timeout=15
    )
    scanner.scan()

except (KeyboardInterrupt, SystemExit):
    logger.warning("Waiting for scanner shutdown")

except Exception as e:
    logger.error("[ERR] %s" % e)
    error_log = LoggerWrapper(args.error_log)
    error_log.error(e)

#     'b8:d5:0b:ac:c1:2e': 'JBL-Charge-3',
#     # 'cb:5a:bb:cc:cb:33': 'Risto-Keys',  # Trackr
#     'e2:da:83:48:32:e1': 'Magda-Keys',
#     'e9:0c:ed:40:39:75': 'Trackr3',
#     '1d:34:92:ef:c4:62': 'Laptop-X240-Magda',
#     '9c:b6:d0:d3:18:fe': 'Laptop-XPS13-Risto',
#     'd4:80:9d:44:ab:f0': 'MX-Master-Mouse',
#     '48:4b:aa:16:03:8d': 'iPhone-Risto',
#     '31:15:7b:05:69:87': 'Kindle',
#     '64:a7:69:60:1f:7d': 'HTC-Wildfire-Zygmunt',
#     '34:7c:15:04:91:66': 'Waga-Media-Tech',
#     '18:7a:93:05:1c:a3': 'Passat-Ble',  # Blue
#     '18:7a:93:05:7e:bb': 'Risto-Keys'