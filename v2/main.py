import requests
from urllib.parse import urljoin

import fastapi, uvicorn
from typing import Dict, Literal, Union

from . import Objects

class ExtraArgumentsError(Exception):
    pass

class EventHandler:
    def __init__(self):
        self.on_text_message = None
        self.on_image_message = None
        self.on_message = None

    def handle(self, data:dict):
        try:
            data = Objects.parse_event(data)
            if isinstance(data, Objects.Messages.Message):
                if isinstance(data, Objects.Messages.TextMessage):
                    print(f'[TextMessage] [{data.sender.id} -> {data.channel.id}] {data.content}')
                    for i in CommandTree.prefixes.keys():
                        if data.content.startswith(i):
                            cmd = CommandTree.prefixes[i].parse(data)
                            if cmd is not None:
                                Client._instance.send_text(
                                    channel = data.channel,
                                    content = str(cmd())
                                )
                                return
                    if self.on_text_message is not None:
                        self.on_text_message(data)
                        return
                elif isinstance(data, Objects.Messages.ImageMessage):
                    if self.on_image_message is not None:
                        self.on_image_message(data)
                        return
                if self.on_message is not None:
                    self.on_message(data)
                    return

        except NotImplementedError:
            return

class CommandTree:
    prefixes = {}
    class Argument:
        def __init__(self, var_type:Union[str, int, float, bool], description:str):
            self.var_type = var_type
            self.description = description

    def __init__(self, prefix:str):
        assert ' ' not in prefix
        assert prefix not in self.prefixes.keys()
        self.prefix = prefix
        self.prefixes[prefix] = self
        self.commands = {}
        self.help = 'Oops sorry there is no help here :('

    def command(self, cmd_name:str = None):
        def decorator(func:callable):
            name = cmd_name if cmd_name is not None else func.__name__
            name = name.strip()
            assert not ' ' in name
            self.commands[name] = func
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def parse(self, data:Objects.Messages.TextMessage):
        target = data.content[len(self.prefix):]
        elements = target.split(' ')
        if elements[0] in self.commands.keys():
            command = self.commands[elements[0]]
            return lambda: command(*elements[1:], **{'interaction': data})
        else:
            return None

class Client:
    _instance = None
    def __init__(self, base_url:str, download_url:str, app_id:str):
        assert self._instance is None
        Client._instance = self
        #Validate the link
        self.session = requests.Session()
        try:
            self.session.get(base_url).raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise ConnectionRefusedError(f'{base_url}is a invalid link') from e

        #Storing the params
        self.base_url = urljoin(base_url, 'v2/api/')
        self.app_id = app_id
        self.session.headers.update(
            {
                'Content-Type': 'application/json'
            }
        )

        Objects.Messages.RequestConfig.Session = self.session
        Objects.Messages.RequestConfig.app_id = app_id
        Objects.Messages.RequestConfig.url = self.base_url
        Objects.Messages.RequestConfig.download_url = download_url

        #Attaining the token from the url
        response = self.session.post(
            urljoin(self.base_url, 'tools/getTokenId'),
            data = {}
        )
        response.raise_for_status()
        self.token = response.json()['data']
        self.session.headers.update(
            {
                'Content-Type': 'application/json',
                'X-GEWE-TOKEN': self.token
            }
        )

        #Starting the event handler
        self.event_handler = EventHandler()

        #Setting up the FastAPI callback server
        self.app = fastapi.FastAPI()
        @self.app.post('/')
        def runtime(data:Dict):
            self.event_handler.handle(data)
            return fastapi.responses.PlainTextResponse(
                'Jinitaimei :D',
                status_code = 200,
            )

    def run(self, port:int = 2533):
        uvicorn.run(
            self.app,
            host = '0.0.0.0',
            port = port
        )

    def event(self, target):
        def decorater(func:callable):
            assert hasattr(self.event_handler, target)
            self.event_handler.__setattr__(target, func)

            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorater

    def send_text(self, channel:Objects.Misc.Channel, content:str, mention:list[Objects.Misc.User] | str = []):
        ats = []
        if isinstance(mention, list):
            for i in mention:
                assert isinstance(i, Objects.Misc.User)
                ats.append(i)
        elif isinstance(mention, str):
            if 'all' in mention:
                ats.append('notify@all')

        response = self.session.post(
            urljoin(self.base_url, 'message/postText'),
            json = {
                'appId': self.app_id,
                'toWxid': channel.id,
                'content': content,
                'ats': ','.join(ats)
            }
        )
        response.raise_for_status()
        response = response.json()
        if response['ret'] != 200:
            raise requests.exceptions.HTTPError(response)
