class User:
    _instances = []
    def __init__(self, id:str):
        self.id = id
        self._instances.append(self)

class Channel:
    _instances = []
    def __init__(self, id:str):
        self.id = id
        self.dm = not self.id.endswith('@chatroom')
        self._instances.append(self)

    @property
    def is_dm(self):
        return self.dm

    @property
    def is_chatroom(self):
        return not self.dm