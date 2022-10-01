from my_http.http_constants.response_codes import BAD_REQUEST, HTTP_VERSION_NOT_SUPPORTED
from my_http.http_constants.http_methods import GET
from my_http.data_types import HttpRequest, _HttpResponse, HttpResponse
from my_socketserver import BaseRequestHandler
from config import ENCODING
from controllers import CONTROLLER_MANAGER_INSTANCE


class HttpHandler(BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.controller_manager = CONTROLLER_MANAGER_INSTANCE
        self.HTTP_VERSION = "HTTP/1.1"
        super().__init__(request, client_address, server)

    def handle(self):
        data = ""
        while True:
            data += str(self.request.recv(1024), ENCODING)
            if HttpHandler.check_if_all_data_is_recieved(data) is True:
                break

        valid_request = True
        try:
            http_request = self.decode_data(data)
        except IndexError:
            valid_request = False

        if valid_request is True:
            if http_request.http_version != self.HTTP_VERSION:
                valid_request = False

        if valid_request:
            response = self.find_implementation_and_execute(http_request)
            response = _HttpResponse(self.HTTP_VERSION, response.status_code, response.headers, response.body)

        else:
            status = HTTP_VERSION_NOT_SUPPORTED
            headers = {"Content-Length": str(0)}
            body = ""
            response = _HttpResponse(status, headers, body, self.HTTP_VERSION)
        
        a = response.make_response_string()
        self.request.send(response.make_response_string())


    def check_if_all_data_is_recieved(data):
        if data == "" or data is None:
            return False

        if len(data.split("\r\n\r\n")) == 1:
            return False

        body_length = None
        for line in data.split("\r\n\r\n")[0].split("\r\n"):
            if "Content-Length" in line:
                line = line.split(":")
                body_length = int(line[1])
        
        method = data.split("\r\n")[0].split(" ")[0]
        if body_length is None and method != GET.upper():
            return False

        if body_length is None and method == GET.upper():
            return True
        
        if len(data.split("\r\n\r\n")[1]) == body_length:
            return True


    def decode_data(self, data):
        http_method = None
        route_mapping = None
        http_version = None
        headers = dict()
        body = None

        data = data.split("\r\n")

        http_method = data[0].split(" ")[0]
        route_mapping = data[0].split(" ")[1]
        http_version = data[0].split(" ")[2]
        
        headers_portion = list()
        for idx, line in enumerate(data):
            if line == "":
                headers_portion = data[1:idx]
                body = data[idx+1:]
                break
        
        aux = body
        body = ""
        for line in aux:
            body += line + "\r\n"
        body = body[:-2]

        for line in headers_portion:
            line = line.split(": ")
            headers[line[0]] = line[1]

        return HttpRequest(http_method, route_mapping, http_version, headers, body, self.client_address, self.server)


    def find_implementation_and_execute(self, http_request):
        result = self.controller_manager.find_implementation_and_execute(http_request)
        if result is None:
            body = "Path not found"
            headers = {"Content-Length": str(len(body))}
            result = HttpResponse(BAD_REQUEST, headers, body)

        return result