from utils.exceptions import *
import json
import os

class Config():
    def __init__(self):
        self.token = self._read()
        
    def _read(self):
        if not os.path.exists("./config.json"):
            raise NoConfigException()
        
        file = open("./config.json", "r")
        config = json.loads(file.read())
        file.close()
        
        if not "token" in config:
            raise WrongConfigException()
        
        return config["token"]