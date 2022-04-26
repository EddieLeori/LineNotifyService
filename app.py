from flask import Flask, request, abort
from lib.utility import *
import requests
import os
import json

class LineNotifyService:
    def __init__(self):
        self.name = "LineNotifyService"
        self.host = ""
        self.port = int(os.environ.get('PORT', 99999))
        self.content_type = ""
        self.tokens = []
        self.line_rul = ""
        self.is_init = False
        if self.init() is False:
            return
        
        self.app = Flask(__name__)
        self.app.add_url_rule("/check", methods=['POST'], view_func= self.check) 
        self.app.add_url_rule("/callback", methods=['POST'], view_func= self.callback) 
        # self.app.add_url_rule("/action", methods=['POST'], view_func= self.action)

        self.actions = {
            "notify": self.notify,
            "notifyAll": self.notifyAll
        }

        self.is_init = True
        self.notifyAll(self.name + " start..")

    def init(self):
        try:
            with open('option.json', 'r') as f:
                cfg = json.load(f)
                f.close()
                Log(cfg)
                if self.name not in cfg:
                    return
                if "host" in cfg[self.name]:
                    self.host = cfg[self.name]["host"]
                if "port" in cfg[self.name]:
                    self.port = cfg[self.name]["port"]
                if "Content-Type" in cfg[self.name]:
                    self.content_type = cfg[self.name]["Content-Type"]
                if "tokens" in cfg[self.name]:
                    self.tokens = cfg[self.name]["tokens"]
                if "line_url" in cfg[self.name]:
                    self.line_rul = cfg[self.name]["line_url"]
        except:
            Log("LineNotifyService init eror!")
            return False
        return True

    def check(self):
        text = 'check ok!'
        return text

    def callback(self):
            return 'OK'

    def run(self):
        if self.is_init is False:
            return
        self.app.run(self.host, self.port)

    def notify(self, token, str):
        msg = str
        headers = {
                "Authorization": "Bearer " + token,
                "Content-Type": self.content_type
            }
        playload = { 'message': msg}
        r = requests.post(
            self.line_rul, 
            headers = headers, 
            params = playload)
        return r.status_code

    def notifyAll(self, str):
        msg = str
        for token in self.tokens:
            response = self.notify(token, str)
            if response is not 200:
                Log("error " + response + " " + token + " " + str)
                return False
        return True

if __name__ == "__main__":

    service = LineNotifyService()
    service.run()


