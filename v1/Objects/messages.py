from abc import ABC, abstractmethod

import base64
from datetime import datetime

class Message(ABC):
    @abstractmethod
    def __init__(self, content, channel, sender, receiver):
        return

    @staticmethod
    def parse(data:dict):
        obj = None
        if data['TypeName'] == 'AddMsg':
            if data['Data']['MsgType'] == 1:
                obj = TextMessage.from_json(
                    data['Data']
                )
            elif  data['Data']['MsgType'] == 3:
                obj = ImageMessage.from_json(
                    data['Data']
                )
        if obj is not None:
            obj.app_id = data['Appid']
            obj.Wxid = data['Wxid']
        return obj

class TextMessage(Message):
    """
    AddMsg:1
    """
    from .entities import User, Channel
    def __init__(self, *, content:str, channel:Channel, sender:User = None):
        self.content = content
        self.channel = channel
        self.sender = sender

    @classmethod
    def from_json(cls, data:dict):
        from .entities import User, Channel
        channel = data['FromUserName']['string']
        if '@chatroom' in channel:
            sender, content = data['Content']['string'].split(':', 2)
            sender = sender.strip()
            content = content.strip()
        else:
            sender = data['FromUserName']['string']
            content = data['Content']['string']
        instance = cls(
            sender = User(sender),
            content = content,
            channel = Channel(channel)
        )
        instance.msg_id = data['MsgId']
        instance.new_msg_id = data['NewMsgId']
        instance.created_time = datetime.fromtimestamp(data['CreateTime']).strftime('%Y-%m-%d %H:%M:%S')
        return instance

class ImageMessage(Message):
    """
    AddMsg:3
    """
    from .entities import User
    def __init__(self, *, content:str, sender:User = None, receiver:User):
        self.raw_cdn = content
        self.sender = sender
        self.receiver = receiver

    @classmethod
    def from_json(cls, data:dict):
        from .entities import User
        instance = cls(
            sender = User(data['FromUserName']['string']),
            receiver = User(data['ToUserName']['string']),
            content = data['Content']['string']
        )
        instance.preview = base64.b64decode(
            data['ImgBuf']['buffer']
        )
        instance.created_time = data['CreateTime']
        instance.msg_id = data['MsgId']
        instance.new_msg_id = data['NewMsgId']
        return instance
