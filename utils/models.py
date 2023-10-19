from discord import Member

class Settings():
    def __init__(self, guild_id: int, text_category_id: int, voice_category_id: int, teams_channel_id: int, team_owner_role_id: int):
        self.guild_id = guild_id
        self.text_category_id = text_category_id
        self.voice_category_id = voice_category_id
        self.teams_channel_id = teams_channel_id
        self.team_owner_role_id = team_owner_role_id

class Team():
    def __init__(self, id: int, role_id: int, guild_id: int, members: list[Member], name: str, owner_id: int, text_channel_id: int, voice_channel_id: int, message_id: int = 0):
        self.id = id
        self.role_id = role_id
        self.guild_id = guild_id
        self.members = members        
        self.name = name
        self.owner_id = owner_id
        self.text_channel_id = text_channel_id
        self.voice_channel_id = voice_channel_id
        self.message_id = message_id