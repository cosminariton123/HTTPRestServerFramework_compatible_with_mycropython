import re

from my_http.http_constants.http_methods import HTTP_METHODS_AS_LIST, GET, POST, PUT, DELETE
from my_http.http_constants.response_codes import convert_code_to_string, BAD_REQUEST
from my_http.data_types import HttpRequest, HttpResponse
from my_socketserver import BaseRequestHandler

class BaseController():
    def __init__(self, base_path=""):
        pattern = re.compile("^__.*__$")
        base_controller_methods_list = list(filter(lambda x:(pattern.match(x) == None) , dir(self.__class__.__bases__[0])))
        methods_list = list(filter(lambda x:(pattern.match(x) == None and x not in base_controller_methods_list) , dir(self)))

        self.methods_dict = dict()
        for method in methods_list:
            self.methods_dict[method] = base_path
        
        errors = self._validate_controller()
        if errors:
            raise ValueError(f"Controller methods do not comply with notation guidelines. Should have one of {HTTP_METHODS_AS_LIST} at the begging of name, delimited with an underscore. Methods which do not comply: {errors}")


    def _validate_controller(self):
        errors = list()
        for method in self.methods_dict:
            if method.split("_")[0] not in HTTP_METHODS_AS_LIST:
                errors.append(method)
        return errors


    def find_implementation(self, http_request):
        pass



class HttpHandler(BaseRequestHandler):
    def __init__(self, controller_class_list):
        self.controller_class_list = controller_class_list
        self.HTTP_VERSION = "HTTP/1.0"

    def handle(self):
        
        data = ""
        while True:
            data += self.request.recv(1024)
            if self.check_if_all_data_is_recieved(data) is True:
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
            status, headers, body = self.find_implementation_and_execute(http_request)

        else:
            status = convert_code_to_string(BAD_REQUEST)
            headers = {"Content-Length": str(0)}
            body = ""
        
        response = HttpResponse(self.HTTP_VERSION, status, headers, body).make_response_string()
        self.request.send(response)


    def check_if_all_data_is_recieved(data):
        if data == "" or data is None:
            return False

        data = data.strip().split("\r\n")
        body_length = None
        for line in data:
            if "Content-Length" in line:
                line = line.split(":")
                body_length = int(line[1])
        
        if body_length is None:
            return False

        if len(data.split("\r\n") < 2):
            return False
        
        if data.split("\r\n")[1] == body_length:
            return True


    def decode_data(data):
        http_method = None
        route_mapping = None
        http_version = None
        headers = dict()
        body = None

        data = data.strip().split("\r\n")

        http_method = data[0].split(" ")[0]
        route_mapping = data[0].split(" ")[1]
        http_version = data[0].split(" ")[2]
        
        for idx, line in enumerate(data):
            if line == "":
                headers_portion = data[1:idx]
                body = data[idx:]

        for line in headers_portion:
            line = line.split(": ")
            headers[line[0]] = line[1]

        return HttpRequest(http_method, route_mapping, http_version, headers, body)


    def find_implementation_and_execute(self, http_request):
        for controller in self.controller_class_list:
            pass