import network
import socket
import time
from machine import Pin

led = Pin("LED", Pin.OUT)

ssid = 'BT Dial Up'
password = '10TheAvenueOnline'

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        led.toggle()
        time.sleep(0.2)