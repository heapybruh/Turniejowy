from discord import Member, Message

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