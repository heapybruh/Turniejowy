import utils
from utils.exceptions import DatabaseNotConnected, UserNotInDatabase
import discord
from datetime import datetime

class Embed:
    def user(member: discord.Member, guild_id: int):
        if (utils.db == None):
            return Embed.error(DatabaseNotConnected().__str__())
            
        team = utils.db.get_member_team(member, guild_id)
        
        if team == None:
            return Embed.error(UserNotInDatabase().__str__())
            
        embed = discord.Embed(color = discord.Colour.from_rgb(255, 255, 255), timestamp = datetime.utcnow())  

        embed.set_author(name = member.name, icon_url = member.avatar.url)
        embed.add_field(name = "Team Name", value = team.name, inline = False)
        embed.add_field(name = "Team Owner", value = f"<@{team.owner_id}>", inline = False)
        embed.add_field(name = "Other Team Members", value = "\n".join([f"<@{x.id}>" if x.id != team.owner_id else "" for x in team.members]), inline = False)

        embed.set_footer(text = f"{utils.cfg.bot_name} by heapy")
        
        return embed
    
    def success(message: str):
        embed = discord.Embed(color = discord.Colour.from_rgb(0, 255, 0), title = "Success!", description = message, timestamp = datetime.utcnow())  
        embed.set_footer(text = f"{utils.cfg.bot_name} by heapy")
        
        return embed
    
    def error(message: str):
        embed = discord.Embed(color = discord.Colour.from_rgb(255, 0, 0), title = "Error!", description = message, timestamp = datetime.utcnow())  
        embed.set_footer(text = f"{utils.cfg.bot_name} by heapy")
        
        return embed