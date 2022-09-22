import json
import time

#TODO WRAPPER FOR SERIALIZABLE
class Message():
    def __init__(self, message=None):
        self.message = None
        self.timestamp = None
        if message is not None:
            self.make_message(message)

    def make_message(self, message):
        self.message = message
        self.timestamp = time.time()
        
    def get_serialized(self):
        return json.dumps({"message": self.message, "timestamp": self.timestamp})