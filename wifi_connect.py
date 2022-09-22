from machine import Pin
import network
import time

def connect_to_internet(SSID, WLAN_KEY):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, WLAN_KEY)

    pin = Pin("LED", Pin.OUT)
    while wlan.isconnected() == False:
        pin.toggle()
        time.sleep(1)
    
    pin.low()
    ip = wlan.ifconfig()[0]
    return ip