from .models import Team, Settings, Bot, TableBase, Member
from typing import Sequence
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

class Database():
    def __init__(self, bot: Bot):
        self.bot = bot
        self._connect()
    
    def _connect(self):
        self._engine = create_engine("sqlite:///database.db")
        self._session = Session(self._engine, expire_on_commit = False)
        TableBase.metadata.create_all(self._engine)
        
    def update_team(self, team: Team):
        statement = select(Team).where(Team.id == team.id)
        
        selected_team = self._session.scalars(statement).one()
        selected_team.name = team.name
        selected_team.members = team.members
        selected_team.message = team.message
        
        self._session.commit()
        
    def add_team(self, team: Team):
        self._session.add(team)
        self._session.commit()
        
    def remove_team(self, role: int, guild: int) -> str:
        statement = select(Team).where((Team.role == role) & (Team.guild == guild))

        selected_team = self._session.scalars(statement).one()
        self._session.delete(selected_team)
        
        self._session.commit()
        
        return selected_team.name
    
    def remove_guild(self, guild: int):
        statement = select(Team).where(Team.guild == guild)
        
        selected_teams = self._session.scalars(statement).all()
        for team in selected_teams:
            self._session.delete(team)
        
        statement = select(Member).where(Member.guild == guild)
        
        selected_members = self._session.scalars(statement).all()
        for member in selected_members:
            self._session.delete(member)
        
        self._session.commit()
            
    def get_team(self, role: int, guild: int) -> Team | None:
        statement = select(Team).where((Team.role == role) & (Team.guild == guild))
        selected_team = self._session.scalars(statement).one_or_none()
        
        return selected_team
    
    def get_all_teams(self) -> Sequence[Team]:
        statement = select(Team)
        selected_teams = self._session.scalars(statement).all()
            
        return selected_teams
    
    def get_member_team(self, member: Member) -> Team | None:
        statement = select(Member).where((Member.discord == member.discord) & (Member.guild == member.guild))
        selected_member = self._session.scalars(statement).one_or_none()

        return selected_member.team if selected_member != None else None
    
    def add_settings(self, settings: Settings):
        self._session.add(settings)
        self._session.commit()
        
    def update_settings(self, settings: Settings):
        statement = select(Settings).where(Settings.guild == settings.guild)
        
        selected_settings = self._session.scalars(statement).one()
        selected_settings.text_category = settings.text_category
        selected_settings.voice_category = settings.voice_category
        selected_settings.team_list_channel = settings.team_list_channel
        selected_settings.team_owner_role = settings.team_owner_role
            
        self._session.commit()
        
    def get_settings(self, guild: int) -> Settings | None:
        statement = select(Settings).where(Settings.guild == guild)
        selected_settings = self._session.scalars(statement).one_or_none()
        
        return selected_settings
    
    def add_to_team(self, member: Member, team: Team):
        statement = select(Team).where(Team.id == team.id)
        selected_team = self._session.scalars(statement).one()
        
        if not member in selected_team.members:
            selected_team.members.append(member)
            self._session.commit()
    
    def remove_from_team(self, member: Member, team: Team):
        statement = select(Team).where(Team.id == team.id)
        selected_team = self._session.scalars(statement).one()
        
        if member in selected_team.members:
            selected_team.members.remove(member)
            self._session.commit()