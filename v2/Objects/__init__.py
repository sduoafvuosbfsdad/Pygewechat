from . import Messages
from . import Misc

import json
import xmltodict

class Utils:
    @staticmethod
    def get_by_id(obj, *, id:str):
        assert obj in [Misc.Channel, Misc.User]
        for i in obj._instances:
            if i.id == id:
                return i
        return obj(id)

def parse_event(data:dict):
    app_id = data['Appid']
    wxid = data['Wxid']
    data = data['Data']
    content = data['Content']['string']
    channel  = Utils.get_by_id(Misc.Channel, id = data['FromUserName']['string'])
    if channel.is_dm:
        sender = Utils.get_by_id(Misc.User, id = data['FromUserName']['string'])
    elif channel.is_chatroom:
        sender, content = content.splt(':', 2)
        sender = Utils.get_by_id(Misc.User, id = sender.id)
    MsgType = data['MsgType']
    created_at = data['CreateTime']
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
            msg_id=msg_id,
            new_msg_id=new_msg_id,
        )
    raise NotImplementedError

__all__ = [Messages, Misc, Utils]