# connection portion taken from raspberry pi website
# projects.raspberrypi.org/en/projects/get-started-pico-w/2
from machine import Pin
import urequests as requests
import network
import socket
from time import sleep
import machine

ssid = 'BU Guest (unencrypted)'

def connect():
    led = Pin(0, Pin.OUT)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid)
    while wlan.isconnected() == False: #wait for handhsake
        print('Waiting')
        sleep(1)
    print(wlan.ifconfig())

try:
    connect()
except KeyboardInterrupt:
    machine.reset()