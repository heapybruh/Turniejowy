class NoConfigException(Exception):
    def __init__(self):
        self.message = "Config file does not exist"
        super().__init__(self.message)
        
class WrongConfigException(Exception):
    def __init__(self):
        self.message = "Config file is wrong, one of required keys is not in the config"
        super().__init__(self.message)
        
class NoAdminException(Exception):
    def __init__(self):
        self.message = "You don't have **__Administrator__** permission!"
        super().__init__(self.message)