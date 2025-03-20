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

class ChatRoom(Channel):
    _instances = []
    def __init__(self, id:str):
        assert id.endswith('@chatroom')
        super().__init__(id)
        Channel._instances.append(self)

class DirectMessages(Channel):
    _instances = []
    def __init__(self, id:str):
        assert not id.endswith('@chatroom')
        super().__init__(id)
        Channel._instances.append(self)
