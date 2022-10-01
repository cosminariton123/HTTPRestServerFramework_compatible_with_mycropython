from my_http.http_handler import HttpHandler
from my_socketserver import SocketServer
from config import SSID, WLAN_KEY


import sys

if sys.implementation.name == "micropython":
    from wifi_connect import connect_to_internet
    from machine import Pin

def main():

    if sys.implementation.name == "micropython":
        ip = connect_to_internet(SSID, WLAN_KEY)
        pin = Pin("LED", Pin.OUT)
        pin.high()
    else:
        ip = ""
    address_and_port = (ip, 8000)
    http_server = SocketServer(address_and_port, HttpHandler)
    http_server.serve_forever()

if __name__ == '__main__':
    main()
