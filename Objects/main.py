class User:
    def __init__(self, id:str):
        self.id = id

class BaseInteraction:
    def __init__(self):
        pass

class TextMessage(BaseInteraction):
    def __init__(self, sender:User, recipient:User, content:str):
        super().__init__()
        self.sender = sender
        self.recipient = recipient
        self.content = content

    @classmethod
    def json(cls, data:dict):
        return cls(
            sender = User(data['FromUserName']['string']),
            recipient = User(data['ToUserName']['string']),
            content = data['Content']['string']
        )

def parse_interaction(data:dict):
    msg_type = data['MsgType']
    if msg_type == 1:
        return TextMessage.json(data)