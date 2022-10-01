from machine import Pin
import network
import time

def connect_to_internet(SSID, WLAN_KEY):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, WLAN_KEY)
    print(f"Connecting to \"{SSID}\"", end="")

    pin = Pin("LED", Pin.OUT)
    while wlan.isconnected() == False:
        print(".", end="")
        pin.toggle()
        time.sleep(1)
    
    print(f"\nConnected to \"{SSID}\"")
    pin.low()
    ip = wlan.ifconfig()[0]
    return ip