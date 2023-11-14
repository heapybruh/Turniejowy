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
        
        teams = utils.db.get_all_teams()
        
        if len(teams) >= 1:
            for team in teams:
                try:
                    settings = utils.db.get_settings(guild = team.guild)
                    if not settings:
                        continue
                    
                    guild = discord.utils.get(self.bot.guilds, id = team.guild)
                    if not guild:
                        utils.db.remove_guild(guild = team.guild)
                    
                    teams_channel = discord.utils.get(guild.channels, id = settings.team_list_channel)
                    if not teams_channel:
                        continue
                
                    role = discord.utils.get(guild.roles, id = team.role)
                    if not role:
                        utils.db.remove_team(team.role, team.guild)
                    
                    team.name = role.name
                    message = await teams_channel.fetch_message(team.message)
                    embed = utils.Embed.team(team, role.color)
                    
                    if not message:
                        team_message = await teams_channel.send(embed = embed)
                        team.message = team_message.id
                    else:
                        await message.edit(embed = embed)
                        
                    utils.db.update_team(team)
                except Exception as error:
                    print(f"An error has occurred while refreshing team {team.name}: {error.__str__()}")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(refresh(bot))