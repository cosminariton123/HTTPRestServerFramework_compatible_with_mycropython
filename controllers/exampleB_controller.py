from my_http.base_controller import BaseController
from my_http.http_data_types import HttpResponse
from message import Message

class ExampleBController(BaseController):
    def __init__(self):
        base_path="/ExampleB"
        super().__init__(base_path)
        
        self.methods_dict["get_world"] += "/world"

    def get_world(self, http_request):
        body = Message("Hello world!")
        response = HttpResponse(200, {}, body)
        return response

