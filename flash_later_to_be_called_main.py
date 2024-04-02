from my_framework.my_http.http_handler import HttpHandler
from my_framework.my_socketserver.my_socketserver import SocketServer
from config import SSID, WLAN_KEY, PORT

import sys

if sys.implementation.name == "micropython":
    from my_machine import pie_pico_w_instance

def main():
    global pie_pico_w_instance
    if sys.implementation.name == "micropython":
        ip = pie_pico_w_instance.connect_to_internet(SSID, WLAN_KEY)
        pie_pico_w_instance.onboard_led_on()
    else:
        ip = ""

    address_and_port = (ip, PORT)
    http_server = SocketServer(address_and_port, HttpHandler)
    http_server.serve_forever()

if __name__ == '__main__':
    main()
