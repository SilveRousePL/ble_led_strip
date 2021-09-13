import bleak
import asyncio
import logging
from threading import Thread

class BluetoothDevice:
    def __init__(self, address) -> None:
        self.log = logging.getLogger(__name__)
        self.loop = asyncio.get_event_loop()
        def bleak_thread(loop):
            asyncio.set_event_loop(loop)
            loop.run_forever()
        self.t = Thread(target=bleak_thread, args=(self.loop,))
        self.t.start()
        self.address = address
        self.client = bleak.BleakClient(address)
        self.log.info(f'Bluetooth device instance created! Address: {self.address}')

    def __del__(self):
        self.disconnect()
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.log.info(f'Bluetooth device instance removed! Address: {self.address}')

    def get_address(self):
        return self.address

    def connect(self):
        asyncio.run_coroutine_threadsafe(self.__connect(), self.loop)

    def disconnect(self):
        asyncio.run_coroutine_threadsafe(self.__disconnect(), self.loop)

    def send(self, data):
        asyncio.run_coroutine_threadsafe(self.__send(data), self.loop)

    async def __connect(self):
        self.log.debug(f'__connect method')
        try:
            if not self.client.is_connected:
                await self.client.connect()
                self.log.info(f'Connected!')
            else:
                self.log.info(f'Device is already connected!')
        except Exception as e:
            print(e)

    async def __disconnect(self):
        self.log.debug(f'__disconnect method')
        try:
            if self.client.is_connected:
                await self.client.disconnect()
                self.log.info(f'Disconnected!')
            else:
                self.log.warning(f'Device was not connected!')
        except Exception as e:
            print(e)

    async def __send(self, data):
        self.log.debug(f'__send method')
        try:
            if not self.client.is_connected:
                await self.__connect()
            await self.client.write_gatt_char(0x7, bytearray(data))
        except Exception as e:
            print(e)
        finally:
            self.log.info(f'Sent!')
