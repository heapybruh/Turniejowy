class NoConfig(Exception):
    def __init__(self):
        self.message = "Config file does not exist."
        super().__init__(self.message)
        
class WrongConfig(Exception):
    def __init__(self):
        self.message = "Config file is wrong, one of required keys is not in the config."
        super().__init__(self.message)
        
class NoAdmin(Exception):
    def __init__(self):
        self.message = "You don't have **__Administrator__** permission ."
        super().__init__(self.message)
        
class TooSmallTeam(Exception):
    def __init__(self):
        self.message = "The team is too small! Minimum size is 2-stacked team."
        super().__init__(self.message)
        
class TeamNotFound(Exception):
    def __init__(self):
        self.message = "Team not found."
        super().__init__(self.message)
        
class UserNotInDatabase(Exception):
    def __init__(self):
        self.message = "User not found in database."
        super().__init__(self.message)
        
class DatabaseNotConnected(Exception):
    def __init__(self):
        self.message = "Couldn't connect to Database."
        super().__init__(self.message)