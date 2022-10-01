import upip

from wifi_connect import connect_to_internet
from config import SSID, WLAN_KEY

def install(packages):
    ip = connect_to_internet(SSID, WLAN_KEY)
    import upip
    for package in packages:
        upip.install(package)

if __name__ == "__main__":
    install(["traceback"])