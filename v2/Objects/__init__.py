from . import Messages
from . import Misc

import json
import xmltodict

class Utils:
    @staticmethod
    def get_by_id(obj, *, id:str):
        assert obj in [Misc.Channel, Misc.User]
        for i in obj.instances:
            if i.id == id:
                return i
        return obj(i)

def parse_event(data:dict):
    app_id = data['Appid']
    wxid = data['Wxid']
    data = data['Data']
    content = data['Content']['string']
    sender = Utils.get_by_id(Misc.User, id = data['FromUserName']['string'])
    channel = Utils.get_by_id(Misc.Channel, id = data['ToUserName']['string'])
    MsgType = data['MsgType']
    created_at = data['CreateTime']
    push = data['PushContent']
    msg_id = data['MsgId']
    new_msg_id = data['NewMsgId']

    if MsgType == 1:
        return Messages.TextMessage(
            app_id = app_id,
            wxid = wxid,
            content = content,
            sender = sender,
            channel = channel,
            created_at = created_at,
            push = push,
            msg_id = msg_id,
            new_msg_id = new_msg_id,
        )
    elif MsgType == 3:
        return Messages.ImageMessage(
            app_id=app_id,
            wxid=wxid,
            content=content,
            sender=sender,
            channel=channel,
            created_at=created_at,
            push=push,
            msg_id=msg_id,
            new_msg_id=new_msg_id,
        )
    raise NotImplementedError

__all__ = [Messages, Misc, Utils]