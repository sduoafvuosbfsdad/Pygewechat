class User:
    _instances = []
    def __init__(self, id:str):
        self.id = id
        self._instances.append(self)

class Channel:
    _instances = []
    def __init__(self, id:str):
        self.id = id
        self._instances.append(self)