import tools
from tools import Team, NoAdminException
import discord
from discord import app_commands
from discord.ext import commands

class team(commands.GroupCog, name = "team"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.checks.cooldown(1, 1, key = lambda i: (i.guild.id))
    @app_commands.describe(
        member_1 = "Select user.",
        member_2 = "Select user.",
        member_3 = "Select user.",
        member_4 = "Select user.",
        member_5 = "Select user.",
        team_name = "Enter team's name."
    )
    @app_commands.command(
        name = "add5", 
        description = "Adds a 5-stacked team to Database"
    )
    async def add5(
        self,
        interaction: discord.Interaction,
        member_1: discord.Member,
        member_2: discord.Member,
        member_3: discord.Member,
        member_4: discord.Member,
        member_5: discord.Member,
        team_name: str
    ):
        try:
            if not interaction.user.guild_permissions.administrator:
                raise NoAdminException()
                
            team_id = tools.db.last_team_id() + 1
            team = Team(team_id, interaction.guild_id, [member_1, member_2, member_3, member_4, member_5], team_name, member_1.id)
            tools.db.add_team(team)
            
            embed = tools.Embed.success(f"Successfully added team **{team_name}**!")
            await interaction.response.send_message(embed = embed)
        except Exception as error:
            await interaction.response.send_message(f"Error: {error}", ephemeral = True)

    @add5.error
    async def on_cooldown_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message("This guild is limited to use this command once per second! Try again in 1s...", ephemeral = True)
            
    @app_commands.checks.cooldown(1, 1, key = lambda i: (i.guild.id))
    @app_commands.describe(
        member_1 = "Select user.",
        member_2 = "Select user.",
        member_3 = "Select user.",
        team_name = "Enter team's name."
    )
    @app_commands.command(
        name = "add3", 
        description = "Adds a 3-stacked team to Database"
    )
    async def add3(
        self,
        interaction: discord.Interaction,
        member_1: discord.Member,
        member_2: discord.Member,
        member_3: discord.Member,
        team_name: str
    ):
        try:
            if not interaction.user.guild_permissions.administrator:
                raise NoAdminException()
                
            team_id = tools.db.last_team_id() + 1
            team = Team(team_id, interaction.guild_id, [member_1, member_2, member_3], team_name, member_1.id)
            tools.db.add_team(team)
            
            embed = tools.Embed.success(f"Successfully added team **{team_name}**!")
            await interaction.response.send_message(embed = embed)
        except Exception as error:
            await interaction.response.send_message(f"Error: {error}", ephemeral = True)

    @add3.error
    async def on_cooldown_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message("This guild is limited to use this command once per second! Try again in 1s...", ephemeral = True)
            
    @app_commands.checks.cooldown(1, 1, key = lambda i: (i.guild.id))
    @app_commands.describe(team_id = "Enter team's id.")
    @app_commands.command(
        name = "delete", 
        description = "Deletes a team from Database"
    )
    async def delete(
        self,
        interaction: discord.Interaction,
        team_id: int
    ):
        try:
            if not interaction.user.guild_permissions.administrator:
                raise NoAdminException()
                
            team = tools.db.get_team(team_id, interaction.guild_id)
            
            if team == None:
                await interaction.response.send_message("Team not found!", ephemeral = True)
                return
                
            team_name = tools.db.remove_team(team_id)
            
            embed = tools.Embed.success(f"Successfully removed team **{team_name}**!")
            await interaction.response.send_message(embed = embed)
        except Exception as error:
            await interaction.response.send_message(f"Error: {error}", ephemeral = True)

    @delete.error
    async def on_cooldown_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message("This guild is limited to use this command once per second! Try again in 1s...", ephemeral = True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(team(bot))