import upip

from wifi_connect import connect_to_internet

def install(packages):
    ip = connect_to_internet()
    import upip
    for package in packages:
        upip.install(package)

if __name__ == "__main__":
    install(["importlib"])