# Simple single threaded HTTP server

It is designed to run on small applications.
Makes development and testing easy even on headless machines.

## How to use the framework

### Configuration files

Edit config.py file or create and edit config_info_that_shouldnt_appear_on_git.py as per your liking.
Be warned that only "utf-8" ENCODING was tested.
Be warned that only the default CONTROOLERS_FOLDER_PATH was tested. You should definetly copy **init**.py to the new directory.

PORT should be a number.
SSID should be a string with the Wifi name. Set it to a random or empty string if not used on a Raspberry Pi Pico W.
WLAN_KEY should be a string with the Wifi password. Set it to a random or empty string if not used on a Raspberry Pi Pico W.
PRODUCTION should be a boolean True | False.

#### Examples Raspberry Pi Pico W

PORT = 1234
SSID = "MyAwesomeWify"
WLAN_KEY = "mySecureWifiPassword"
PRODUCTION = False

#### Examples non Raspberry Pi Pico W

PORT = 1234
SSID = ""
WLAN_KEY = ""
PRODUCTION = False

### Controllers

Create controller files or edit the existing ones in controllers directory.
The structure and implementations should be simillar to the examples provided in controllers directory.
