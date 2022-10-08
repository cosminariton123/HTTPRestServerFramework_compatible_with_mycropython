from machine import Pin
import network
import time

class PiePicoW():
    def __init__(self):
        pass

    def connect_to_internet(self, SSID, WLAN_KEY):
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
    
    def onboard_led_on(self):
        pin = Pin("LED", Pin.OUT)
        pin.high()

    def onboard_led_off(self):
        pin = Pin("LED", Pin.OUT)
        pin.low()

    def onboard_led_toggle(self):
        pin = Pin("LED", Pin.OUT)
        pin.toggle()

pie_pico_w_instance = PiePicoW()
