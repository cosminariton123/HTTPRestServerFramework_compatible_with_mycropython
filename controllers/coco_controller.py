from my_http.http_handler import BaseController

class CocoController(BaseController):
    def __init__(self):
        base_path="/Coco"
        super().__init__(base_path)
        
        self.methods_dict["get_world"] += "/world"

    def get_world(self, coco):
        print(5/0)
        return 5

