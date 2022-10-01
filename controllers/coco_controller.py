from my_http.base_controller import BaseController
from my_http.data_types import HttpResponse
from message import Message

class CocoController(BaseController):
    def __init__(self):
        base_path="/Coco"
        super().__init__(base_path)
        
        self.methods_dict["get_world"] += "/world"
        self.methods_dict["post_power"] += "/power/{value}"

    def get_world(self, http_request):
        print(5)
        response = HttpResponse(200, {"Content-Length": str(0)}, "")
        return response

    def post_power(self, http_request):
        body = int(self.get_path_variables(http_request.path)["value"]) ** 2
        body = Message(str(body))
        response = HttpResponse(200, {}, body)
        return response

