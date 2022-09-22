from ast import comprehension
import re

from my_http.http_constants.http_methods import HTTP_METHODS_AS_LIST, GET, POST, PUT, DELETE
from my_http.http_constants.response_codes import convert_code_to_string, BAD_REQUEST
from my_http.data_types import HttpRequest, HttpResponse
from my_socketserver import BaseRequestHandler

class BaseController():
    def __init__(self, base_path=""):
        self.methods_list = self._get_methods_list()

        self.methods_dict = dict()
        for method in self.methods_list:
            self.methods_dict[method] = base_path
        
        self._validate_http_methods_notation()


    def _get_methods_list(self):
        pattern = re.compile("^__.*__$")
        base_controller_methods_list = list(filter(lambda x:(pattern.match(x) == None) , dir(BaseController)))
        methods_list = list(filter(lambda x:(pattern.match(x) == None and x not in base_controller_methods_list) , dir(self)))
        return methods_list


    def _validate_http_methods_notation(self):
        for method in self.methods_dict:
            if method.split("_")[0] not in HTTP_METHODS_AS_LIST:
                raise ValueError(f" \"{method}\" method from controller: \"{self.__class__.__name__}\" should have one of {HTTP_METHODS_AS_LIST} at the begging of name, delimited with an underscore.")


    def validate_methods_dict(self):        
        for method in self.methods_list:
            try:
                self.methods_dict[method]
            except KeyError:
                raise ValueError(f"Method \"{method}\" does not have a path set in controller \"{self.__class__.__name__}\" initialization.")

        for method, path in self.methods_dict.items():
            if method not in self.methods_list:
                raise ValueError(f"Method \"{method}\" declared in controller \"{self.__class__.__name__}\" initialization, does not exist")



    def validate_paths(self, other_controllers):
        def validate_the_2_paths_for_ambiguity(method, path, other_controller, other_method, other_path):
            pattern = re.compile(re.sub("{.*}", ".*", path))
            if pattern.match(other_path) is not None:
                comprehensive_error_dict = {"controller" : self.__class__.__name__, "method" : method, "path" : path}
                comprehensive_error_dict_other = {"controller" : other_controller.__class__.__name__, "method" : other_method, "path" : other_path}
                raise ValueError(f"Path ambiguity detected between: {comprehensive_error_dict} and {comprehensive_error_dict_other}")

        for idx, (method, path) in enumerate(self.methods_dict.items()):
            for other_method, other_path in list(self.methods_dict.items())[:idx] + list(self.methods_dict.items())[idx + 1:]:
                validate_the_2_paths_for_ambiguity(method, path, self, other_method, other_path)

            for other_controller in other_controllers:
                for other_method, other_path in other_controller.methods_dict.items():
                    validate_the_2_paths_for_ambiguity(method, path, other_controller, other_method, other_path)


    #TODO IMPLEMENT THIS
    def find_implementation(self, http_request):
        pass



class HttpHandler(BaseRequestHandler):
    def __init__(self, controller_manager):
        self.controller_manager = controller_manager
        self.HTTP_VERSION = "HTTP/1.0"
        self.super.__init__()

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


    #TODO: implement
    def find_implementation_and_execute(self, http_request):
        if self.controller_manager.find_implementation_and_execute(http_request) == False:
            return False