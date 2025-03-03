import json
import requests
from .Objects import entities, messages

class EventHandler:
    def __init__(self):
        self.commands = self.Commands('!')
        self.commands.header = '!'
        self.on_message = None

    def handle(self, event):
        if isinstance(event, messages.Message):
            if isinstance(event, messages.TextMessage):
                #Check if it is a command
                command = self.commands.parse(event.content)
                if command is not None:
                    pass
                else:
                    if self.on_message is not None:
                        self.on_message(event)

    def event(self, name:str):
        def decorator(func):
            if name == 'on_message' and self.on_message is  None:
                self.on_message = func
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

    class Commands:
        def __init__(self, header:str):
            self.header = header
            self._commands = []

        def parse(self, text:str):
            return None

        def commands(self, name:str):
            def decorator(func):
                self._commands.append(
                    self.Command(
                        name = name,
                        target = func
                    )
                )
                def wrapper(*args, **kwargs):
                    return func(*args, **kwargs)
                return wrapper
            return decorator

        class Command:
            def __init__(self, name:str, target:callable):
                self.name = name
                self.callable = target

            def __call__(self, *args, **kwargs):
                print('Command called!')
                return self.Call(*args, **kwargs)

            class Call:
                def __init__(self, target:callable, *args, **kwargs):
                    self.args = args
                    self.kwargs = kwargs
                    self.target = target

                def __call__(self):
                    return self.target(*self.args, **self.kwargs)

class Client:
    def __init__(self, base_url:str):
        self.event_handler = EventHandler()

        self.base_url = base_url
        #Attain the token from the api
        self.token = self._post(
            '/tools/getTokenId',
            payload = {},
            header={}
        )['data']

    def send(self, channel:entities.Channel, app_id:str, message:str):
        """
        This function helps to send messages to people.

        :warning: Currently you can only send text messages. This under development.
        :param receiver:
        :param message:
        :return:
        """
        self._post(
            '/message/postText',
            {
                'appId': app_id,
                'toWxid': channel.id,
                'content': message
            }
        )

    def _post(self, path:str, payload:dict, header:dict = None, *, default_header:bool = True):
        """
        Internal method to send POST request to gewe api.

        :param path:
        :param payload:
        :param header:
        :param default_header:
        :return: The json of the response.
        :rtype: dict
        """
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
        return response.json()
