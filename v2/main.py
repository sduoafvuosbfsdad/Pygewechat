import json
import requests
from urllib.parse import urljoin

import fastapi, uvicorn
from typing import Dict

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

        #Setting up the FastAPI callback server
        self.app = fastapi.FastAPI()
        @self.app.post('/')
        def runtime(data:Dict):
            print(data)
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
