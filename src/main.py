#!/usr/bin/python3
import logging
import bleak
import asyncio
import sys
from threading import Thread
from request_processor import json_to_action

debug = True
log = logging.getLogger(__name__)
if debug:
    log.setLevel(logging.DEBUG)
    h = logging.StreamHandler(sys.stdout)
    h.setLevel(logging.DEBUG)
    log.addHandler(h)


async def send(address, data):
    client = bleak.BleakClient(address)
    try:
        await client.connect()
        await client.write_gatt_char(0x7, bytearray(data))
    except Exception as e:
        print(e)
    finally:
        await client.disconnect()


def send_data(address, data):
    asyncio.run_coroutine_threadsafe(send(address, data), loop)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    def bleak_thread(loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()
    t = Thread(target=bleak_thread, args=(loop,))
    t.start()

    # TODO: Listening UDP
    while True:
        # Examples: 
        # {"device": "ELK-BLEDOM   ", "command": "power", "value": "0"}
        # {"device": "ELK-BLEDOM   ", "command": "brightness", "value": "30"}
        # {"device": "ELK-BLEDOM   ", "command": "color_rgb", "value": "ffffff"}
        # {"device": "ELK-BLEDOM   ", "command": "effect", "value": "GRADIENT_RGBYCMW"}
        data = input('Input JSON: ')
        data = json_to_action(data)
        send_data(data[0], data[1])

    loop.call_soon_threadsafe(loop.stop)
