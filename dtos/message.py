from my_framework.serializable import Serializable
import json

class Message(Serializable):
    def __init__(self, message=None):
        try:
            self.message = json.loads(message)["message"]
        except:
            self.message = message
            