import socket

class SocketServer():
    def __init__(self, address_and_port, RequestHandlerClass, controller_manager):
        self.address_and_port = address_and_port
        self.RequestHandlerClass = RequestHandlerClass
        self.controller_manager = controller_manager
        self.server = socket.socket()

    def serve_forever(self):
        self.server.bind(self.address_and_port)
        print(f"Binded at: {self.address_and_port}")
        self.server.listen()

        while True:
            self.accept()

    def accept(self):
        request, client_address = self.server.accept()

        self.RequestHandlerClass(request, client_address, self.server, self.controller_manager)

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
        self.request.close()
