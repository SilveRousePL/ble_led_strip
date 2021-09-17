#!/usr/bin/python3
import logging
import socket
import sys, os
import time
import config
import bluetooth
from request_processor import get_action, data_validator

class Receiver:
    def __init__(self, udp_ip, udp_port) -> None:
        self.log = logging.getLogger(__name__)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((udp_ip, udp_port))
        self.log.info(f'UDP socket bound on {udp_ip}:{udp_port}')

        self.last_pass_time = time.time()  # TODO: Replace to better solution

    def recv(self):
        while True:
            self.log.debug('Waiting for datagram...')
            data, addr = self.sock.recvfrom(1024)
            self.log.info(f'Datagram recv from {addr}')
            self.log.debug(f'Data: {data}')

            now = time.time()
            time_interval = 0.1
            if now - self.last_pass_time > time_interval:
                self.last_pass_time = now
            else:
                self.log.debug(f'Dropped data ({now - self.last_pass_time} <= {time_interval})')
                continue

            if not data_validator(data):
                self.log.warning(f'Invalid data received')
                continue
            else:
                return data


class App:
    def __init__(self) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info('Running application')
        udp_ip = config.get_config()['server']['ip']
        udp_port = config.get_config()['server']['port']
        self.receiver = Receiver(udp_ip, udp_port)
        self.bt_devices = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.bt_devices.clear()

    def loop(self):
        received_data = self.receiver.recv()
        data = get_action(received_data)
        device = [d for d in self.bt_devices if d.get_address() == data[0]]
        if len(device) == 0:
            self.log.info(f'BT device with address {data[0]} was not used')
            device = bluetooth.BluetoothDevice(data[0])
            self.bt_devices.append(device)
            device.send(data[1])
        else:
            device[0].send(data[1])

    def run(self):
        try:
            while True:
                self.loop()
        except KeyboardInterrupt:
            self.log.info('KeyboardInterrupt detected! Closing app...')
            return


def excepthook(exc_type, exc_value, traceback):
    from traceback import print_exception
    log = logging.getLogger()
    log.error("Logging an uncaught exception",
            exc_info=(exc_type, exc_value, traceback))
    print_exception(exc_type, exc_value, traceback)
    print(f'Logs file is available in {log.handlers[0].baseFilename}')

if __name__ == "__main__":
    from datetime import datetime
    if not os.path.exists('logs'):
        os.makedirs('logs')
    logging.basicConfig(
        filename=f'logs/{datetime.now().strftime("%Y%m%d%H%M%S")}.log',
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.DEBUG
    )
    sys.excepthook = excepthook
    with App() as app:
        app.run()
    print() # Additional line after closed app
