from flask import Flask, request, jsonify
import logging
import traceback

class server:
    def __init__(self, handler:callable):
        self.app = Flask(__name__)
        self.handler = handler
        self.paths()

    def paths(self):
        @self.app.route('/', methods = ['GET', 'POST'])
        def main():
            try:
                data = request.get_json()
                logging.debug(f'Received request: {data}')
                self.handler(data)
            except Exception as e:
                print(e)
                traceback.print_exc()
            return jsonify({'ret':200, 'msg':'Sigma'}), 200

    def run(self):
        self.app.run(host='0.0.0.0', port=8080)