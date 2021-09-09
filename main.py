#!/usr/bin/python3
import pygatt
import sys, os

adapter = pygatt.GATTToolBackend()
handle = 0x7
value = [0x7e,0x00,0x05,0x03,0x00,0xff,0x00,0x00,0xef] # set green color

try:
    adapter.start()
    list_of_devices = adapter.scan()
    print(list_of_devices)
    number = int(input("Type number: "))
    device = adapter.connect(list_of_devices[number]['address'])
    value = device.char_write_handle(handle, value)
finally:
    adapter.stop()

