import requests
from urllib.parse import urljoin

import fastapi, uvicorn
from typing import Dict, Literal

import Objects

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

class Client:
    def __init__(self, base_url:str, app_id:str):
        #Validate the link
        self.session = requests.Session()
        try:
            self.session.get(base_url).raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise ConnectionRefusedError(f'{base_url}is a invalid link') from e

        #Storing the params
        self.base_url = urljoin(base_url, '/v2/api')
        self.app_id = app_id
        self.session.headers.update(
            {
                'Content-Type': 'application/json'
            }
        )

        Objects.Messages.RequestConfig.Session = self.session
        Objects.Messages.RequestConfig.app_id = app_id
        Objects.Messages.RequestConfig.url = self.base_url

        #Attaining the token from the url
        response = self.session.post(
            urljoin(base_url, '/tools/getTokenId'),
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
            host = 'localhost',
            port = port
        )

    def event(self, target:Literal['on_message']):
        def decorater(func:callable):
            assert hasattr(self.event_handler, target)
            self.event_handler.__setattr__(target, func)

            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorater