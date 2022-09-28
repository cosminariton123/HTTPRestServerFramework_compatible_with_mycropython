import json

#TODO WRAPPER FOR SERIALIZABLE
class Message():
    def __init__(self, message=None):
        self.message = None
        if message is not None:
            self.make_message(message)

    def make_message(self, message):
        self.message = message
        
    def serialize(self):
        return json.dumps({"message": self.message})