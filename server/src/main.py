#!/usr/bin/python3
import logging
import socket
import sys, os
import config
import bluetooth
from request_processor import get_action


def main():
    log = logging.getLogger(__name__)
    sys.excepthook = excepthook
    log.info('Running application')
    bt_devices = []

    udp_ip = config.get_config()['server']['ip']
    udp_port = config.get_config()['server']['port']
    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_DGRAM)
    sock.bind((udp_ip, udp_port))
    log.info(f'UDP socket bound on {udp_ip}:{udp_port}')

    while True:
        try:
            log.debug('Waiting for datagram...')
            data, addr = sock.recvfrom(1024)
            log.info(f'Datagram recv from {addr}')
            log.debug(f'Data: {data}')
            data = get_action(data)
            device = [d for d in bt_devices if d.get_address() == data[0]]
            if len(device) == 0:
                log.info(f'BT device with address {data[0]} was not used. Creating instance...')
                device = bluetooth.BluetoothDevice(data[0])
                bt_devices.append(device)
                device.send(data[1])
            else:
                device[0].send(data[1])            
        except KeyboardInterrupt:
            log.info('KeyboardInterrupt detected! Closing app...')
            bt_devices.clear()
            break
    log.info('Closed')


def excepthook(excType, excValue, traceback):
    log = logging.getLogger()
    log.error("Logging an uncaught exception",
            exc_info=(excType, excValue, traceback))
    print(traceback.format_exc())


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
    main()
    print() # Additional line after closed app
