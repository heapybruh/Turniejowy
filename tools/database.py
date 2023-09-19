import sqlite3
from discord import Member
from discord.ext import commands

class Team():
    def __init__(self, id: int, guild_id: int, members: list[Member], name: str, owner_id: int):
        self.id = id
        self.guild_id = guild_id
        self.members = members        
        self.name = name
        self.owner_id = owner_id

class Database():
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.connect()
    
    def connect(self):
        self.database = sqlite3.connect("database.sqlite3")
        self.cursor = self.database.cursor()
        
        self.cursor.execute("CREATE TABLE IF NOT EXISTS teams(id INTEGER, guild_id INTEGER, name TEXT, owner_id INTEGER, UNIQUE(id))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS members(discord_id INTEGER, guild_id INTEGER, team_id INTEGER, UNIQUE(discord_id, guild_id))")
        self.database.commit()
        
        print("[✓] Connected to database")
        
    def add_team(self, team: Team):
        self.cursor.execute("INSERT OR IGNORE INTO teams VALUES(?, ?, ?, ?)", (team.id, team.guild_id, team.name, team.owner_id))
        for member in team.members:
            self.cursor.execute("INSERT OR IGNORE INTO members VALUES(?, ?, ?)", (member.id, team.guild_id, team.id))
        self.database.commit()
        
    def remove_team(self, team_id: int) -> str:
        self.cursor.execute("SELECT * FROM teams WHERE id = ?", (team_id, ))
        team = self.cursor.fetchall()
        team_name = team[0][2]
        
        self.cursor.execute("DELETE FROM teams WHERE id = ?", (team_id, ))
        self.cursor.execute("DELETE FROM members WHERE team_id = ?", (team_id, ))
        self.database.commit()
        
        return team_name
    
    def get_member_team(self, member: Member, guild_id: int) -> Team | None:
        self.cursor.execute("SELECT * FROM members WHERE discord_id = ? AND guild_id = ?", (member.id, guild_id))
        user = self.cursor.fetchall()
        
        if len(user) == 0:
            return None
        
        team_id = user[0][2]
        self.cursor.execute("SELECT * FROM teams WHERE id = ?", (team_id, ))
        team = self.cursor.fetchall()
        team_name = team[0][2]
        team_owner_id = team[0][3]
        
        self.cursor.execute("SELECT * FROM members WHERE team_id = ?", (team_id, ))
        members = self.cursor.fetchall()
        guild = self.bot.get_guild(guild_id)
        
        team = Team(team_id, guild_id, [guild.get_member(x[0]) for x in members], team_name, team_owner_id)
        
        return team
    
    def last_team_id(self) -> int:
        self.cursor.execute("SELECT * FROM teams")
        teams = self.cursor.fetchall()
        
        return len(teams)
