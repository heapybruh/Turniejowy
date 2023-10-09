import utils
import discord
from datetime import datetime

class Embed:
    def user(member: discord.Member, guild_id: int):
        if (utils.db == None):
            embed = discord.Embed(color = discord.Colour.from_rgb(255, 0, 0), title = "Couldn't connect to Database", timestamp = datetime.utcnow())
            embed.set_footer(text = f"{utils.cfg.bot_name} by heapy")
            return embed
            
        team = utils.db.get_member_team(member, guild_id)
        
        if team == None:
            embed = discord.Embed(color = discord.Colour.from_rgb(255, 0, 0), title = "User not found in Database", timestamp = datetime.utcnow())
            embed.set_footer(text = f"{utils.cfg.bot_name} by heapy")
            return embed
            
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