import socket

class SocketServer():
    def __init__(self, address_and_port, RequestHandlerClass):
        self.address_and_port = address_and_port
        self.RequestHandlerClass = RequestHandlerClass
        self.server = socket.socket()

    def server_forever(self):
        self.server.bind(self.address_and_port)
        self.server.listen()

        while True:
            self.accept()

    def accept(self):
        request, client_address = self.server.accept()

        handler = self.RequestHandlerClass(request, client_address, self.server)
        handler.handle()
        request.close()

class BaseRequestHandler:
    def __init__(self, request, client_address, server):
        self.request = request
        self.client_address = client_address
        self.server = server
        self.setup()
        try:
            self.handle()
        finally:
            self.finish()

    def setup(self):
        pass

    def handle(self):
        pass

    def finish(self):
        pass
