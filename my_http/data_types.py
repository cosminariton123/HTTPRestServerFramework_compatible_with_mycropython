from my_http.http_constants.response_codes import get_http_status_by_number, RESPONSE_CODES_LIST, INTERNAL_SERVER_ERROR
from config import ENCODING

class HttpRequest():
    def __init__(self, http_method, route_mapping, http_version, headers, body, client_address, server):
        self.http_method = http_method
        self.route_mapping = route_mapping
        self.http_version = http_version
        self.headers = headers
        self.body = body
        self.client_address = client_address
        self.server = server

class HttpResponse():
    def __init__(self, status_code, headers, body):
        def error(status):
            self.status_code = status
            self.headers = {"Content-Length": str(0)}
            self.body = ""
            return

        if status_code not in RESPONSE_CODES_LIST:
            try:
                status_as_integer = int(status_code)
                if get_http_status_by_number(status_as_integer) is None:
                    error(INTERNAL_SERVER_ERROR)
            except:
                error(INTERNAL_SERVER_ERROR)
        if type(headers) is not dict:
            error(INTERNAL_SERVER_ERROR)
        try:
            body = body.serialize()
        except:
            error(INTERNAL_SERVER_ERROR)

        self.status_code = str(status_code)
        self.headers = headers
        self.body = str(body)

class _HttpResponse():
    def __init__(self, http_version, status_code, headers, body):
        self.http_version = str(http_version)
        self.status_code = str(status_code)
        self.headers = headers
        self.body = str(body)

    def make_response_string(self):
        response = self.http_version + " "
        response += self.status_code + "\r\n"

        for header in self.headers:
            response += str(header) + ": " + str(self.headers[header]) + "\r\n"
        response += "\r\n"

        response += self.body

        return bytes(response, ENCODING)