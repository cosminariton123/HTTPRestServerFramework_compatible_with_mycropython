from my_framework.my_http.base_controller import BaseController
from my_framework.my_http.http_data_types import HttpResponse
from dtos.message import Message

class ExampleAController(BaseController):
    def __init__(self):
        base_path="/ExampleA"
        super().__init__(base_path)
        
        self.methods_dict["get_world"] += "/world"
        self.methods_dict["post_world"] += "/world/path_variable/{name}"
        self.methods_dict["put_query_param"] += "world/query"
        self.methods_dict["delete_body"] += "world/body"

    def get_world(self, http_request):
        body = Message("Hello world!")
        response = HttpResponse(200, {}, body)
        return response

    def post_world(self, http_request):
        name = self.get_path_variables(http_request.path)["name"]
        body = Message(f"Hello {name}! I'm using path variables!")
        response = HttpResponse(200, {}, body)
        return response

    def put_query_param(self, http_request):
        name = self.get_query_param(http_request.path)["name"]
        body = Message(f"Hello {name}! I'm using query parameters!")
        response = HttpResponse(200, {}, body)
        return response

    def delete_body(self, http_request):
        name = Message(http_request.body)
        body = Message(f"Hello {name.message}! I'm using body!")
        response = HttpResponse(200, {}, body)
        return response
