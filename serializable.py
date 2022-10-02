import json

class Serializable():
    def __str__(self):
        return json.dumps(self.__dict__)