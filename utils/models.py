import utils
import discord
from discord.ext import commands
from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship

class TableBase(DeclarativeBase):
    pass

class Settings(TableBase):
    __tablename__ = "settings"
    
    id: Mapped[int] = mapped_column(primary_key = True)
    guild: Mapped[int] = mapped_column()
    text_category: Mapped[int] = mapped_column()
    voice_category: Mapped[int] = mapped_column()
    team_list_channel: Mapped[int] = mapped_column()
    team_owner_role: Mapped[int] = mapped_column()

class Team(TableBase):
    __tablename__ = "team"
    
    id: Mapped[int] = mapped_column(primary_key = True)
    role: Mapped[int] = mapped_column()
    guild: Mapped[int] = mapped_column()
    members: Mapped[List["Member"]] = relationship(back_populates = "team", cascade = "all, delete-orphan")
    name: Mapped[str] = mapped_column()
    owner: Mapped[int] = mapped_column()
    text_channel: Mapped[int] = mapped_column()
    voice_channel: Mapped[int] = mapped_column()
    message: Mapped[int] = mapped_column(default = 0)
    
class Member(TableBase):
    __tablename__ = "member"
    
    id: Mapped[int] = mapped_column(primary_key = True)
    discord: Mapped[int] = mapped_column()
    guild: Mapped[int] = mapped_column()
    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))
    
    team: Mapped["Team"] = relationship(back_populates = "members")
        
class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.presences = True
        intents.members = True

        super().__init__(
            command_prefix = "/", 
            intents = intents)

    async def setup_hook(self):
        for file in utils.Cogs.get():
            if file.is_dir():
                continue
            
            extension = f"cogs.{file.stem}"
            await self.load_extension(extension)
            print(f"Loaded {extension}")

    async def on_ready(self):
        await self.tree.sync()
        await self.change_presence(activity = discord.Activity(type = discord.ActivityType.playing, name = "Helping with Discord Tournaments..."))
        utils.db = utils.Database(self)
        print(f"Discord.py v{discord.__version__} → {self.user} ({self.user.id})")