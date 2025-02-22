#Basic imports
import os
import time
import json
import logging

import base64
import requests

from threading import Thread

from .server import server
from . import Objects

logger = logging.getLogger()

class GeWechatClient:
    _instance = None
    def __init__(
            self,
            base_url:str,
            app_id:str = '',
            uuid:str = '',
            skip_init:bool = False,
    ):
        """
        The Gewechat wrapper client.

        :param base_url: The url to the gewechat api.
        :type base_url: str
        :param app_id: The app id of the gewechat api, leave empty to generate one.
        :type app_id: str
        """
        try:
            #Check for singleton
            if self._instance is not None:
                raise RuntimeError('This class is a singleton')

            #Initialise the client
            logger.info('Client Initialising')

            #Define all variables here to avoid confusion
            self.base_url = base_url
            self.app_id = app_id
            self.default_header = {}
            self.token = ''
            self.server = None
            self.callback_server = None
            self.events = EventHandler()
            self.uuid = uuid

            #Attain Token
            self.token = self.post('/tools/getTokenId')['data']
            self.default_header['Content-Type'] = 'application/json'
            self.default_header['X-GEWE-TOKEN'] = self.token

            self.server = server(self.event_handler)
            self.callback_server = Thread(target=self.server.run)
            self.callback_server.start()

            if not skip_init:
                #Attempt login
                self.login()

                #Start the callback server
                self.server = server(self.event_handler)
                self.set_callback('http://192.168.3.61:8080')
                print(self.app_id, self.uuid)

        except Exception as e:
            logger.error(e)
            raise e

    def event(self, event:str):
        def decorator(func):
            self.events.__setattr__(event, func)
            logger.info(f'Set {event} to {func}')
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def mainloop(self):
        while True:
            time.sleep(1)

    def post(self, url:str, data:str = '{}', headers:dict = None):
        if headers is None:
            headers = self.default_header
        logger.debug(f'Sending POST request with params: url={url}, data={data}, headers={headers}')
        response = requests.post(
            self.base_url + url,
            data = data,
            headers = headers
        )
        logger.debug(f'Responded with {response.json()}')
        if response.status_code != 200:
            raise ConnectionError(f'Error in sending request!{response.status_code}: {response.text}')
        #Convert the response to json
        response = response.json()
        return response

    def event_handler(self, data:dict):
        event = Objects.parse_interaction(
            data['Data']
        )
        if isinstance(event, Objects.TextMessage):
            self.events.on_message(event)

    def login(self):
        response = self.post(
            '/login/getLoginQrCode',
            data = json.dumps(
                {
                    'appId': self.app_id,
                }
            )
        )
        #Check if it is logged in already
        if not(response['ret'] == 500 and response['msg'] == '微信已登录，请勿重复登录。'):
            logger.info('Not logged in. Please login now.')
            with open('login.jpg', 'wb') as f:
                f.write(
                    base64.b64decode(
                        response['data']['qrImgBase64'][21:]
                    )
                )
            os.startfile('login.jpg')
            self.uuid = response['data']['uuid']
            self.app_id = response['data']['appId']

        else:
            logger.info('Already logged in. No action required')

        while True:
            #Check if logged in
            response = self.post(
                '/login/checkLogin',
                data = json.dumps(
                    {
                        'appId': self.app_id,
                        'uuid': self.uuid,
                    }
                )
            )
            if response['ret'] == 500:
                if response['msg'] == '已登录成功，请勿重复操作':
                    logger.debug('Login successful.')
                    break
                else:
                    raise Exception('Failed to login' + response['msg'])
            logger.debug(response['msg'])

    def set_callback(self, ip_address:str):
        response = self.post(
            '/tools/setCallback',
            data = json.dumps(
                {
                    'token': self.token,
                    'callbackUrl':ip_address
                }
            )
        )
        if response['ret'] != 200:
            raise Exception('Failed to set callback')

    def send_message(self, recepient:Objects.User, content:str):
        response = self.post(
            '/message/postText',
            data = json.dumps(
                {
                    'appId': self.app_id,
                    'toWxid': recepient.id,
                    'content': content
                }
            )
        )
        if response['ret'] != 200:
            raise Exception('Failed to send message')

class EventHandler:
    def __init__(self):
        self.on_message = print
