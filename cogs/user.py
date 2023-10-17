import utils
from utils import CommandLimitReached, TeamNotFound, UserNotInDatabase, UserAlreadyInTeam, UserNotInSpecifiedTeam, UserIsTeamOwner, TeamUnderstaffed, NoAdmin
import discord
from discord import app_commands
from discord.ext import commands

class user(commands.GroupCog, name = "user"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.checks.cooldown(1, 1, key = lambda i: (i.guild.id))
    @app_commands.describe(
        user = "Select user."
    )
    @app_commands.command(
        name = "check", 
        description = "Returns info about user from Database"
    )
    async def check(
        self,
        interaction: discord.Interaction,
        user: discord.Member
    ):
        try:
            embed = utils.Embed.user(user, interaction.guild_id)
            await interaction.response.send_message(embed = embed)
        except Exception as error:
            embed = utils.Embed.error(error.__str__())
            await interaction.response.send_message(embed = embed, ephemeral = True)

    @check.error
    async def on_cooldown_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            embed = utils.Embed.error(CommandLimitReached().__str__())
            await interaction.response.send_message(embed = embed, ephemeral = True)
            
    @app_commands.checks.cooldown(1, 1, key = lambda i: (i.guild.id))
    @app_commands.describe(
        user = "Select user.",
        team_role = "Select team's role."
    )
    @app_commands.command(
        name = "add", 
        description = "Adds user to team"
    )
    async def add(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        team_role: discord.Role
    ):
        try:
            if not interaction.user.guild_permissions.administrator:
                raise NoAdmin()
            
            team = utils.db.get_team(team_role.id, interaction.guild_id)
            if not team:
                raise TeamNotFound()
            
            member_team = utils.db.get_member_team(user, interaction.guild_id)
            if member_team:
                raise UserAlreadyInTeam()
            
            await user.add_roles(team_role)
            utils.db.add_to_team(user, team)
            
            embed = utils.Embed.success(f"Successfully added {user.mention} to **{team.name}**!")
            await interaction.response.send_message(embed = embed)
        except Exception as error:
            embed = utils.Embed.error(error.__str__())
            await interaction.response.send_message(embed = embed, ephemeral = True)

    @add.error
    async def on_cooldown_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            embed = utils.Embed.error(CommandLimitReached().__str__())
            await interaction.response.send_message(embed = embed, ephemeral = True)
            
    @app_commands.checks.cooldown(1, 1, key = lambda i: (i.guild.id))
    @app_commands.describe(
        user = "Select user.",
        team_role = "Select team's role."
    )
    @app_commands.command(
        name = "delete", 
        description = "Removes user from team"
    )
    async def delete(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        team_role: discord.Role
    ):
        try:
            if not interaction.user.guild_permissions.administrator:
                raise NoAdmin()
            
            team = utils.db.get_team(team_role.id, interaction.guild_id)
            if not team:
                raise TeamNotFound()
            
            if team.owner_id == user.id:
                raise UserIsTeamOwner()
            
            if (len(team.members) - 1) == 1:
                raise TeamUnderstaffed()
            
            member_team = utils.db.get_member_team(user, interaction.guild_id)
            if not member_team:
                raise UserNotInDatabase()
            
            if team.id != member_team.id:
                raise UserNotInSpecifiedTeam()

            await user.remove_roles(team_role)
            utils.db.remove_from_team(user, team)
            
            embed = utils.Embed.success(f"Successfully removed {user.mention} from **{team.name}**!")
            await interaction.response.send_message(embed = embed)
        except Exception as error:
            embed = utils.Embed.error(error.__str__())
            await interaction.response.send_message(embed = embed, ephemeral = True)

    @delete.error
    async def on_cooldown_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            embed = utils.Embed.error(CommandLimitReached().__str__())
            await interaction.response.send_message(embed = embed, ephemeral = True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(user(bot))