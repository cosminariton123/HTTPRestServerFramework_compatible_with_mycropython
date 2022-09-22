from controllers import ControllerManager
from my_http.http_handler import HttpHandler
from my_socketserver import SocketServer
#from wifi_connect import connect_to_internet
from config import SSID, WLAN_KEY

def main():
    #address_and_port = connect_to_internet(SSID, WLAN_KEY)
    address_and_port = ("", 8000)
    http_server = SocketServer(address_and_port, HttpHandler, ControllerManager())
    http_server.serve_forever()

if __name__ == '__main__':
    main()
