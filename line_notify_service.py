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
        self.psw = ""
        self.is_init = False
        if self.init() is False:
            return
        
        self.app = Flask(__name__)
        self.app.add_url_rule("/check", methods=['POST'], view_func= self.check) 
        self.app.add_url_rule("/callback", methods=['POST'], view_func= self.callback) 
        self.app.add_url_rule("/action", methods=['POST'], view_func= self.action)

        self.actions = {
            "notify": self.notify,
            "notifyAll": self.notifyAll,
            "notifyImgs": self.notifyImgs
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
                if "psw" in cfg[self.name]:
                    self.psw = cfg[self.name]["psw"]
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
        for token in self.tokens:
            response = self.notify(token, str)
            if response != 200:
                Log("error:response={0}, token={1}, str={2}".format(response, token, str))
                return False
        return True
    
    def notifyImgs(self, strdata):
        try:
            imgs = eval(strdata)
            image_files = []
            for img in imgs:
                for token in self.tokens:
                    headers = {
                        "Authorization": "Bearer " + token
                        # "Content-Type": "multipart/form-data"
                    }
                    r = requests.post(
                        self.line_rul, 
                        headers = headers, 
                        params = {
                            "message": "For you!",
                            "imageThumbnail": img,  # 設定圖片縮圖 URL
                            "imageFullsize": img,  # 設定圖片原始大小 URL
                            },
                        files = image_files
                        )
                    if r.status_code != 200:
                        Log("notifyImgs error:{0}", r.status_code)
                        return False
            return True
        except Exception as e:
            Log("notifyImgs error:" + str(e))
            return False
        
    def isAllow(self, psw):
        return psw == self.psw

    def action(self):
        try:
            data = request.data
            obj = json.loads(data)
            print(obj)
            print(type(obj))
            psw = obj["psw"]
            key = obj["key"]
            if self.isAllow(psw) is True:
                if self.actions.get(key) is not None:
                    self.actions[key](obj["value"])
                    Log(obj)
                    return "ok"
            else:
                Log("action not Allow!")
        except Exception as e:
            Log("action except!:{0}".format(e))
        return "error!"


