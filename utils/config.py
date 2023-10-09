from utils.exceptions import *
import json
import os

class Config():
    def __init__(self):
        self.token, self.bot_name = self._read()
        
    def _read(self):
        if not os.path.exists("./config.json"):
            raise NoConfig()
        
        file = open("./config.json", "r")
        config = json.loads(file.read())
        file.close()
        
        if not "token" in config:
            raise WrongConfig()
        
        if not "bot_name" in config:
            config["bot_name"] = "Turniejowy"
        
        return config["token"], config["bot_name"]