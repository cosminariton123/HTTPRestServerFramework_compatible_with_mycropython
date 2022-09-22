from my_http.http_handler import BaseController

class CocoController(BaseController):
    def __init__(self):
        base_path="/Coco"
        super().__init__(base_path)
        
        self.methods_dict["post_power"] += "/power"
        self.methods_dict["get_world"] += "/{coco}"
        self.methods_dict["put_racaciunga"] += "/racaciunga"

    def post_power(self, b, c=5):
        print(c)
        return self.a ** b

    def get_world(self):
        print("World")

    def put_racaciunga(self):
        print("racaciunga")
