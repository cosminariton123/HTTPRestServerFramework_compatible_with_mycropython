from my_framework.serializable import Serializable

class ErrorMessage(Serializable):
    def __init__(self, message=None):
        self.message = message
