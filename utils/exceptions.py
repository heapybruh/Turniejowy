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
        self.message = "You don't have Administrator permission."
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
        
class CommandLimitReached(Exception):
    def __init__(self):
        self.message = "This guild is limited to use this command once per second! Try again in 1s..."
        super().__init__(self.message)
        
class BotNotSetUp(Exception):
    def __init__(self):
        self.message = "Bot is not ready! Use /settings setup to set it up."
        super().__init__(self.message)
        
class WrongRoleColor(Exception):
    def __init__(self):
        self.message = "Provided string is not a color in HEX."
        super().__init__(self.message)
        
class RoleNotFound(Exception):
    def __init__(self):
        self.message = "Team's role doesn't exist."
        super().__init__(self.message)
        
class UserAlreadyInTeam(Exception):
    def __init__(self):
        self.message = "User is already in a team."
        super().__init__(self.message)
        
class UserNotInSpecifiedTeam(Exception):
    def __init__(self):
        self.message = "User not found in specified team."
        super().__init__(self.message)
        
class UserIsTeamOwner(Exception):
    def __init__(self):
        self.message = "User is an owner of that team."
        super().__init__(self.message)
    
class TeamUnderstaffed(Exception):
    def __init__(self):
        self.message = "Teams can only be 2-stacked and above."
        super().__init__(self.message)