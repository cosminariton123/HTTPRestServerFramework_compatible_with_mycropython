from my_http.http_handler import BaseController
from my_http.data_types import HttpResponse

class CocoController(BaseController):
    def __init__(self):
        base_path="/Coco"
        super().__init__(base_path)
        
        self.methods_dict["get_world"] += "/world"

    def get_world(self, http_request):
        print(5)
        response = HttpResponse(200, {"Content-Length": str(0)}, "")
        return response

