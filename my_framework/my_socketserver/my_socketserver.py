import socket

class SocketServer():
    def __init__(self, address_and_port, RequestHandlerClass):
        self.address_and_port = address_and_port
        self.RequestHandlerClass = RequestHandlerClass
        self.server = socket.socket()

    def serve_forever(self):
        self.server.bind(self.address_and_port)
        print(f"Binded at: {self.address_and_port}")
        self.server.listen()

        while True:
            self.accept()

    def accept(self):
        request, client_address = self.server.accept()
        print(f"Serving client: {client_address}")
        self.RequestHandlerClass(request, client_address, self.server)
