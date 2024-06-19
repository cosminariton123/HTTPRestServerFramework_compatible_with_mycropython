from machine import Pin
import machine
import network
import time

class PiePicoW():
    def __init__(self):
        pass

    def connect_to_internet(self, SSID, WLAN_KEY, IFCONFIG=None):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.config(pm = 0xa11140)
        if IFCONFIG is not None:
            wlan.ifconfig(IFCONFIG)

        wlan.connect(SSID, WLAN_KEY)
        print(f"Connecting to \"{SSID}\"", end="")

        pin = Pin("LED", Pin.OUT)
        i = 0
        while wlan.isconnected() == False:
            print(".", end="")
            pin.toggle()
            time.sleep(1)

            i += 1
            if i > 10:
                self.onboard_led_flicker(30, 0.1)
                machine.reset()
        
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

    def onboard_led_flicker(self, times, interval):
        for _ in range(times):
            self.onboard_led_toggle()
            time.sleep(interval)


    def is_connected(self):
        return network.WLAN(network.STA_IF).isconnected()

    def reset(self):
        machine.reset()

pie_pico_w_instance = PiePicoW()