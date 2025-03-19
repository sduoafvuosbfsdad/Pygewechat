import json
import requests
from .Objects import entities, messages

class Client:
    def __init__(self, base_url:str, token:str, app_id:str):
        self.base_url = base_url
        self.token = token
        self.app_id = app_id

    def send(self, receiver:entities.User, message:str):
        self._post(
            '/message/postText',
            {
                'appId': self.app_id,
                'toWxid': receiver.id,
                'content': message
            }
        )

    def _post(self, path:str, payload:dict, header:dict = None, *, default_header:bool = True):
        response = requests.post(
            self.base_url + path,
            data = json.dumps(payload),
            headers = header if header is not None else (
                {
                    'Content-Type': 'application/json',
                    'X-GEWE-TOKEN': self.token
                } if default_header else {'Content-Type': 'application/json'}
            )
        )
        response.raise_for_status()
        if response.json()['ret'] != 200:
            raise Exception(response.json()['msg'])
