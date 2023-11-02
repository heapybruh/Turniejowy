from .models import Team, Settings, Bot
import sqlite3
from discord import Member

class Database():
    def __init__(self, bot: Bot):
        self.bot = bot
        self.connect()
    
    def connect(self):
        self.database = sqlite3.connect("database.sqlite3")
        self.cursor = self.database.cursor()
        
        self.cursor.execute("CREATE TABLE IF NOT EXISTS teams(id INTEGER, role_id INTEGER, guild_id INTEGER, name TEXT, owner_id INTEGER, text_channel_id INTEGER, voice_channel_id INTEGER, message_id INTEGER, UNIQUE(id))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS members(discord_id INTEGER, guild_id INTEGER, team_id INTEGER, UNIQUE(discord_id, guild_id))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS settings(guild_id INTEGER, text_category_id INTEGER, voice_category_id INTEGER, teams_channel_id INTEGER, team_owner_role_id INTEGER, UNIQUE(guild_id))")
        self.database.commit()
        
        print("[✓] Connected to database")
        
    def update_team(self, team: Team):
        self.cursor.execute("UPDATE teams SET name = ?, text_channel_id = ?, voice_channel_id = ?, message_id = ? WHERE id = ?", (team.name, team.text_channel_id, team.voice_channel_id, team.message_id, team.id))
        self.database.commit()
        
    def add_team(self, team: Team):
        self.cursor.execute("INSERT OR IGNORE INTO teams VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (team.id, team.role_id, team.guild_id, team.name, team.owner_id, team.text_channel_id, team.voice_channel_id, team.message_id))
        for member in team.members:
            self.cursor.execute("INSERT OR IGNORE INTO members VALUES(?, ?, ?)", (member.id, team.guild_id, team.id))
        self.database.commit()
        
    def remove_team(self, role_id: int, guild_id: int) -> str:
        self.cursor.execute("SELECT * FROM teams WHERE role_id = ? AND guild_id = ?", (role_id, guild_id))
        team = self.cursor.fetchall()
        team_id = team[0][0]
        team_name = team[0][3]
        
        self.cursor.execute("DELETE FROM teams WHERE id = ?", (team_id, ))
        self.cursor.execute("DELETE FROM members WHERE team_id = ?", (team_id, ))
        self.database.commit()
        
        return team_name
    
    def remove_guild_teams(self, guild_id: int):
        self.cursor.execute("DELETE FROM teams WHERE guild_id = ?", (guild_id, ))
        self.cursor.execute("DELETE FROM members WHERE guild_id = ?", (guild_id, ))
        self.database.commit()

    def get_team(self, role_id: int, guild_id: int) -> Team | None:
        self.cursor.execute("SELECT * FROM teams WHERE role_id = ? AND guild_id = ?", (role_id, guild_id))
        team = self.cursor.fetchall()
        
        if len(team) == 0:
            return None
        
        team_id = team[0][0]
        team_name = team[0][3]
        team_owner_id = team[0][4]
        text_channel_id = team[0][5]
        voice_channel_id = team[0][6]
        message_id = team[0][7]
        
        self.cursor.execute("SELECT * FROM members WHERE team_id = ?", (team_id, ))
        members = self.cursor.fetchall()
        guild = self.bot.get_guild(guild_id)
        
        team = Team(team_id, role_id, guild_id, [guild.get_member(x[0]) for x in members], team_name, team_owner_id, text_channel_id, voice_channel_id, message_id)
        
        return team
    
    def get_all_teams(self) -> list[Team]:
        self.cursor.execute("SELECT * FROM teams")
        teams_fetched = self.cursor.fetchall()
        
        teams = []
        for team in teams_fetched:
            team_id = team[0]
            role_id = team[1]
            guild_id = team[2]
            team_name = team[3]
            team_owner_id = team[4]
            text_channel_id = team[5]
            voice_channel_id = team[6]
            message_id = team[7]
            
            self.cursor.execute("SELECT * FROM members WHERE team_id = ?", (team_id, ))
            members = self.cursor.fetchall()
            guild = self.bot.get_guild(guild_id)
            
            team = Team(team_id, role_id, guild_id, [guild.get_member(x[0]) for x in members], team_name, team_owner_id, text_channel_id, voice_channel_id, message_id)
            teams.append(team)
        
        return teams
    
    def get_member_team(self, member: Member, guild_id: int) -> Team | None:
        self.cursor.execute("SELECT * FROM members WHERE discord_id = ? AND guild_id = ?", (member.id, guild_id))
        user = self.cursor.fetchall()
        
        if len(user) == 0:
            return None
        
        team_id = user[0][2]
        self.cursor.execute("SELECT * FROM teams WHERE id = ?", (team_id, ))
        team = self.cursor.fetchall()
        team_role_id = team[0][1]
        team_name = team[0][3]
        team_owner_id = team[0][4]
        text_channel_id = team[0][5]
        voice_channel_id = team[0][6]
        message_id = team[0][7]
        
        self.cursor.execute("SELECT * FROM members WHERE team_id = ?", (team_id, ))
        members = self.cursor.fetchall()
        guild = self.bot.get_guild(guild_id)
        
        return Team(team_id, team_role_id, guild_id, [guild.get_member(x[0]) for x in members], team_name, team_owner_id, text_channel_id, voice_channel_id, message_id)
    
    def last_team_id(self) -> int:
        self.cursor.execute("SELECT id FROM teams ORDER BY id DESC")
        teams = self.cursor.fetchone()
        
        return teams[0]

    def add_settings(self, settings: Settings):
        self.cursor.execute("INSERT OR IGNORE INTO settings VALUES(?, ?, ?, ?, ?)", (settings.guild_id, settings.text_category_id, settings.voice_category_id, settings.teams_channel_id, settings.team_owner_role_id))
        self.database.commit()
        
    def update_settings(self, settings: Settings):
        self.cursor.execute("UPDATE settings SET text_category_id = ?, voice_category_id = ?, teams_channel_id = ?, team_owner_role_id = ? WHERE guild_id = ?", (settings.text_category_id, settings.voice_category_id, settings.teams_channel_id, settings.team_owner_role_id, settings.guild_id))
        self.database.commit()
        
    def get_settings(self, guild_id: int) -> Settings:
        self.cursor.execute("SELECT * FROM settings WHERE guild_id = ?", (guild_id, ))
        settings = self.cursor.fetchall()

        if len(settings) == 0:
            return None
        
        text_category_id = settings[0][1]
        voice_category_id = settings[0][2]
        teams_channel_id = settings[0][3]
        team_owner_role_id = settings[0][4]
        
        return Settings(guild_id, text_category_id, voice_category_id, teams_channel_id, team_owner_role_id)
    
    def add_to_team(self, member: Member, team: Team):
        self.cursor.execute("INSERT OR IGNORE INTO members VALUES(?, ?, ?)", (member.id, team.guild_id, team.id))
        self.database.commit()
    
    def remove_from_team(self, member: Member, team: Team):
        self.cursor.execute("DELETE FROM members WHERE discord_id = ? AND guild_id = ? AND team_id = ?", (member.id, team.guild_id, team.id))
        self.database.commit()