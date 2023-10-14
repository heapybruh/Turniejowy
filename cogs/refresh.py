import utils
import discord
from discord.ext import commands, tasks
import asyncio

class refresh(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self._refresh.start()

    @tasks.loop(minutes = 30)
    async def _refresh(self):
        await asyncio.sleep(10)
        
        try:
            teams = utils.db.get_all_teams()
            
            for team in teams:
                settings = utils.db.get_settings(team.guild_id)
                if not settings:
                    continue
                
                guild = discord.utils.get(self.bot.guilds, id = team.guild_id)
                if not guild:
                    continue
                
                channel = discord.utils.get(guild.channels, id = settings.teams_channel_id)
                if not channel:
                    continue
            
                role = discord.utils.get(guild.roles, id = team.role_id)
                if not role:
                    continue
                
                message = await channel.fetch_message(team.message_id)
                if not message:
                    continue
                
                embed = utils.Embed.team(team, role.color)
                await message.edit(embed = embed)
        except Exception as error:
            print(f"An error has occurred while refreshing teams: {error.__str__()}")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(refresh(bot))