import utils
from .exceptions import DatabaseNotConnected, UserNotInDatabase, BotNotSetUp, RoleNotFound
from .models import Team, Member
import discord
from datetime import datetime

class Embed:
    def user(member: discord.Member):
        if utils.db == None:
            return Embed.error(DatabaseNotConnected().__str__())
            
        team = utils.db.get_member_team(Member(discord = member.id, guild = member.guild.id))
        if team == None:
            return Embed.error(UserNotInDatabase().__str__())

        role = discord.utils.get(member.roles, id = team.role)
        if role == None:
            return Embed.error(RoleNotFound().__str__())

        member_list = []
        for x in team.members:
            if x.discord != team.owner:
                member_list.append(f"<@{x.discord}>")
            
        embed = discord.Embed(color = role.color, timestamp = datetime.utcnow())
        embed.set_author(name = member.name, icon_url = member.avatar.url)
        embed.add_field(name = "Team's Name", value = team.name, inline = False)
        embed.add_field(name = "Team's Role", value = f"<@&{team.role}>", inline = False)
        embed.add_field(name = "Team's Owner", value = f"<@{team.owner}>", inline = False)
        embed.add_field(name = "Other Team Members", value = "\n".join(member_list), inline = False)
        embed.set_footer(text = f"{utils.cfg.bot_name} by heapy")
        
        return embed
    
    def settings(guild_id: int):
        settings = utils.db.get_settings(guild_id)
        
        if settings == None:
            return Embed.error(BotNotSetUp().__str__())
        
        embed = discord.Embed(color = discord.Colour.from_rgb(255, 255, 255), title = "Settings", timestamp = datetime.utcnow())
        embed.add_field(name = "Text Channels", value = f"<#{settings.text_category}>", inline = False)
        embed.add_field(name = "Voice Channels", value = f"<#{settings.voice_category}>", inline = False)
        if settings.team_owner_role != 0:
            embed.add_field(name = "Role for Team Owners", value = f"<@&{settings.team_owner_role}>", inline = False)
        embed.set_footer(text = f"{utils.cfg.bot_name} by heapy")
        
        return embed
    
    def team(team: Team, color: discord.Colour):
        member_list = []
        for x in team.members:
            if x.discord != team.owner:
                member_list.append(f"<@{x.discord}>")
                
        embed = discord.Embed(color = color, title = team.name, timestamp = datetime.utcnow())
        embed.add_field(name = "Team's Role", value = f"<@&{team.role}>", inline = False)
        embed.add_field(name = "Team's Owner", value = f"<@{team.owner}>", inline = False)
        embed.add_field(name = "Other Team Members", value = "\n".join(member_list), inline = False)
        embed.set_footer(text = f"{utils.cfg.bot_name} by heapy")
        
        return embed
    
    def loading():
        embed = discord.Embed(color = discord.Colour.from_rgb(255, 255, 255), title = "🔃 Working...", description = "It shouldn't take a lot 😄", timestamp = datetime.utcnow())  
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