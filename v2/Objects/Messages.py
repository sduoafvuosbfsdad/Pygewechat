import requests
from urllib.parse import urljoin

import io
from PIL import Image

class RequestConfig:
    Session = None
    app_id = ''
    base_url = ''

class Message:
    def __init__(
            self,
            app_id: str,
            wxid: str,
            msg_id: str,
            new_msg_id: str,
            sender,
            channel,
            created_at: str,
            push: str,
            content: str,

    ):
        self.app_id = app_id
        self.wxid = wxid
        self.msg_id = msg_id
        self.new_msg_id = new_msg_id
        self.sender = sender
        self.channel = channel
        self.created_at = created_at
        self.push = push
        self.content = content
class MediaMessage(Message):
    pass

class TextMessage(Message):
    MsgType = 1
class ImageMessage(MediaMessage):
    MsgType = 3
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xml = self.content
        self.__delattr__('content')
        # noinspection PyTypeChecker
        self.content = property(self.__content)
        self._content = None

    def __content(self):
        if self._content is not None:
            return self._content
        else:
            response = RequestConfig.Session.post(
                urljoin(RequestConfig.base_url, '/message/downloadImage'),
                data = {
                    'appId': RequestConfig.app_id,
                    'xml': self.xml,
                    'type': 1
                }
            )
            response.raise_for_status()
            response = response.json()
            if response['ret'] != 200:
                raise requests.exceptions.RequestException(
                    'Failed to make download request.'
                )

            response = RequestConfig.Session.get(
                urljoin(RequestConfig.base_url, response['data']['fileUrl']),
            )
            response.raise_for_status()
            self._content = Image.open(
                io.BytesIO(response.content),
            )
            return self._content