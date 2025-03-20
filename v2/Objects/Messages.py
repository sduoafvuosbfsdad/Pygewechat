class Message:
    pass
class MediaMessage(Message):
    pass

class TextMessage(Message):
    def __init__(
            self,
            app_id:str,
            wxid:str,
            msg_id:str,
            new_msg_id:str,
            sender:str,
            receiver:str,
            created_at:str,
            push:str,
            content:str,

    ):
        self.app_id = app_id
        self.wxid = wxid
        self.msg_id = msg_id
        self.new_msg_id = new_msg_id
        self.sender = sender
        self.receiver = receiver
        self.created_at = created_at
        self.push = push
        self.content = content
class NameCard(Message):
    def __init__(
            self,
            app_id: str,
            wxid: str,
            msg_id: str,
            new_msg_id: str,
            sender: str,
            receiver: str,
            created_at: str,
            push: str,
            content: str,

    ):
        self.app_id = app_id
        self.wxid = wxid
        self.msg_id = msg_id
        self.new_msg_id = new_msg_id
        self.sender = sender
        self.receiver = receiver
        self.created_at = created_at
        self.push = push
        self.content = content
class FriendRequest(Message):
    def __init__(
            self,
            app_id: str,
            wxid: str,
            msg_id: str,
            new_msg_id: str,
            sender: str,
            receiver: str,
            created_at: str,
            push: str,
            content: str,

    ):
        self.app_id = app_id
        self.wxid = wxid
        self.msg_id = msg_id
        self.new_msg_id = new_msg_id
        self.sender = sender
        self.receiver = receiver
        self.created_at = created_at
        self.push = push
        self.content = content

class ImageMessage(MediaMessage):
    def __init__(
            self,
            app_id: str,
            wxid: str,
            msg_id: str,
            new_msg_id: str,
            sender: str,
            receiver: str,
            created_at: str,
            push: str,
            content: str,
            preview:str
    ):
        self.app_id = app_id
        self.wxid = wxid
        self.msg_id = msg_id
        self.new_msg_id = new_msg_id
        self.sender = sender
        self.receiver = receiver
        self.created_at = created_at
        self.push = push
        self.content = content
class AudioMessage(MediaMessage):
    def __init__(
            self,
            app_id: str,
            wxid: str,
            msg_id: str,
            new_msg_id: str,
            sender: str,
            receiver: str,
            created_at: str,
            push: str,
            content: str,
            preview:str
    ):
        self.app_id = app_id
        self.wxid = wxid
        self.msg_id = msg_id
        self.new_msg_id = new_msg_id
        self.sender = sender
        self.receiver = receiver
        self.created_at = created_at
        self.push = push
        self.content = content
class VideoMessage(MediaMessage):
    def __init__(
            self,
            app_id: str,
            wxid: str,
            msg_id: str,
            new_msg_id: str,
            sender: str,
            receiver: str,
            created_at: str,
            push: str,
            content: str
    ):
        self.app_id = app_id
        self.wxid = wxid
        self.msg_id = msg_id
        self.new_msg_id = new_msg_id
        self.sender = sender
        self.receiver = receiver
        self.created_at = created_at
        self.push = push
        self.content = content
class EmojiMessage(MediaMessage):
    def __init__(
            self,
            app_id: str,
            wxid: str,
            msg_id: str,
            new_msg_id: str,
            sender: str,
            receiver: str,
            created_at: str,
            push: str,
            content: str,

    ):
        self.app_id = app_id
        self.wxid = wxid
        self.msg_id = msg_id
        self.new_msg_id = new_msg_id
        self.sender = sender
        self.receiver = receiver
        self.created_at = created_at
        self.push = push
        self.content = content
class PublicAccountLinkMessage(MediaMessage):
    def __init__(
            self,
            app_id: str,
            wxid: str,
            msg_id: str,
            new_msg_id: str,
            sender: str,
            receiver: str,
            created_at: str,
            push: str,
            content: str,

    ):
        self.app_id = app_id
        self.wxid = wxid
        self.msg_id = msg_id
        self.new_msg_id = new_msg_id
        self.sender = sender
        self.receiver = receiver
        self.created_at = created_at
        self.push = push
        self.content = content
class FileMessage(MediaMessage):
    def __init__(
            self,
            app_id: str,
            wxid: str,
            msg_id: str,
            new_msg_id: str,
            sender: str,
            receiver: str,
            created_at: str,
            push: str,
            content: str,

    ):
        self.app_id = app_id
        self.wxid = wxid
        self.msg_id = msg_id
        self.new_msg_id = new_msg_id
        self.sender = sender
        self.receiver = receiver
        self.created_at = created_at
        self.push = push
        self.content = content

def parse(data:dict):
    try:
        app_id = data['Appid']
        wxid = data['Wxid']
        if data['TypeName'] == 'AddMsg':
            data = data['Data']
            msg_id = data['MsgId']
            new_msg_id = data['NewMsgId']
            sender = data['FromUserName']['string']
            receiver = data['ToUserName']['string']
            created_at = data['CreateTime']
            push = data['PushContent']
            content = data['Content']['string']
            #Text Messages
            if data['MsgType'] == 1:
                return TextMessage(
                    app_id = app_id,
                    wxid = wxid,
                    msg_id = msg_id,
                    new_msg_id = new_msg_id,
                    sender = sender,
                    receiver = receiver,
                    created_at = created_at,
                    push = push,
                    content = content
                )

            elif data['MsgType'] == 42:
                return NameCard(
                    app_id = app_id,
                    wxid = wxid,
                    msg_id = msg_id,
                    new_msg_id = new_msg_id,
                    sender = sender,
                    receiver = receiver,
                    created_at = created_at,
                    push = push,
                    content = content
                )

            elif data['MsgType'] == 37:
                return FriendRequest(
                    app_id = app_id,
                    wxid = wxid,
                    msg_id = msg_id,
                    new_msg_id = new_msg_id,
                    sender = sender,
                    receiver = receiver,
                    created_at = created_at,
                    push = push,
                    content = content
                )

            elif data['MsgType'] in [3, 34, 43, 47, 49]:
                #Media Messages with Preview
                if data['MsgType'] in [3, 34]:
                    preview = data['ImgBuf']
                    if data['MsgType'] == 3:
                        return ImageMessage(
                            app_id = app_id,
                            wxid = wxid,
                            msg_id = msg_id,
                            new_msg_id = new_msg_id,
                            sender = sender,
                            receiver = receiver,
                            created_at = created_at,
                            push = push,
                            content = content,
                            preview = preview
                        )
                    elif data['MsgType'] == 34:
                        return AudioMessage(
                            app_id = app_id,
                            wxid = wxid,
                            msg_id = msg_id,
                            new_msg_id = new_msg_id,
                            sender = sender,
                            receiver = receiver,
                            created_at = created_at,
                            push = push,
                            content = content,
                            preview = preview
                        )
                #Media Messages without Preview
                elif data['MsgType'] in [43, 47, 49]:
                    if data['MsgType'] == 43:
                        return VideoMessage(
                            app_id = app_id,
                            wxid = wxid,
                            msg_id = msg_id,
                            new_msg_id = new_msg_id,
                            sender = sender,
                            receiver = receiver,
                            created_at = created_at,
                            push = push,
                            content = content
                        )
                    elif data['MsgType'] == 47:
                        return EmojiMessage(
                            app_id = app_id,
                            wxid = wxid,
                            msg_id = msg_id,
                            new_msg_id = new_msg_id,
                            sender = sender,
                            receiver = receiver,
                            created_at = created_at,
                            push = push,
                            content = content,
                        )
                    elif data['MsgType'] == 49:
                        raise NotImplementedError('I need to learn how to parse XML rip me')

        raise NotImplementedError

    except NotImplementedError:
        with open('NotImplementedStuff.txt', 'a') as file:
            file.write(
                data + '\n\n\n\n'
            )
            file.close()
