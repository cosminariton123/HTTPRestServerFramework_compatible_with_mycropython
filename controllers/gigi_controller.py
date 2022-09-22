from my_http.http_handler import BaseController

class GigiController(BaseController):
    def __init__(self):
        base_path="/Gigi"
        super().__init__(base_path)
        
        self.methods_dict["post_gigi"] += "/gigi"

    def post_gigi(self, a):
        print(5)
        return 5

