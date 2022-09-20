class HttpRequest():
    def __init__(self, http_method, route_mapping, http_version, headers, body):
        self.http_method = http_method
        self.route_mapping = route_mapping
        self.http_version = http_version
        self.headers = headers
        self.body = body


class HttpResponse():
    def __init__(self, http_version, status_code, headers, body):
        self.http_version = http_version
        self.status_code = status_code
        self.headers = headers
        self.body = body

    def make_response_string(self):
        response = self.http_version + " "
        response += self.status + "\r\n"

        for header in self.headers:
            response += str(header) + ": " + str(self.headers[header]) + "\r\n"
        response += "\r\n"

        response += self.body

        return response