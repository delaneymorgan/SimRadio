
from flask import Flask, json, jsonify, request
from flask_classful import FlaskView, route

from model import Model


class WebService(FlaskView):
    name:str
    model:Model
    port:int
    debug:bool

    def __init__(self, name:str, model:Model, port=12345, debug=False):
        self.name = name
        self.model = model
        self.port = port
        self.debug = debug
        self.app = Flask(name)
        self.register(self.app, route_base="/")
        return

    def index(self):
        return json.dumps("SimRadio API")

    @route("signal")
    def signal(self):
        if request.method == "GET":
            return str(self.model.get_signal_strength())
        elif request.method == "PUT":
            new_signal = json.loads(request.json)
            self.model.set_signal_strength(new_signal)
            return str(self.model.get_signal_strength())
        return # 400

    @route("mac")
    def mac(self):
        if request.method == "GET":
            return str(self.model.get_mac_address())
        elif request.method == "PUT":
            new_mac = json.loads(request.json)
            self.model.set_mac_address(new_mac)
            return self.model.get_mac_address()
        return

    def run(self):
        self.app.run(debug=self.debug, host='0.0.0.0')
