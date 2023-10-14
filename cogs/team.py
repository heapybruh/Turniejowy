import utils
from utils import NoAdmin, TooSmallTeam, TeamNotFound, CommandLimitReached, BotNotSetUp, WrongRoleColor
from models import Team
import discord
from discord import app_commands
from discord.ext import commands
from PIL import ImageColor
import asyncio

class team(commands.GroupCog, name = "team"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.checks.cooldown(1, 1, key = lambda i: (i.guild.id))
    @app_commands.describe(
        role_color = "Enter role's color in HEX. (example: #ffffff)",
        team_name = "Enter team's name.",
        member_1 = "Select user.",
        member_2 = "Select user.",
        member_3 = "Select user.",
        member_4 = "Select user.",
        member_5 = "Select user.",
        reserve_member_1 = "Select user.",
        reserve_member_2 = "Select user."
    )
    @app_commands.command(
        name = "add", 
        description = "Adds a team (maximum 5-stacked/minimum 2-stacked + 2 reserved) to Database"
    )
    async def add(
        self,
        interaction: discord.Interaction,
        role_color: str,
        team_name: str,
        member_1: discord.Member,
        member_2: discord.Member,
        member_3: discord.Member = None,
        member_4: discord.Member = None,
        member_5: discord.Member = None,
        reserve_member_1: discord.Member = None,
        reserve_member_2: discord.Member = None
    ):
        await interaction.response.send_message(embed = utils.Embed.loading())
        
        try:
            if not interaction.user.guild_permissions.administrator:
                raise NoAdmin()

            settings = utils.db.get_settings(interaction.guild_id)
            if not settings:
                raise BotNotSetUp()

            member_list = list(set([x for x in [member_1, member_2, member_3, member_4, member_5, reserve_member_1, reserve_member_2] if x is not None]))

            if len(member_list) < 2:
                raise TooSmallTeam()
            
            if len(role_color) != 7:
                raise WrongRoleColor()
            
            color = ImageColor.getrgb(role_color)

            role = await interaction.guild.create_role(name = team_name, permissions = discord.Permissions.none(), colour = discord.Color.from_rgb(color[0], color[1], color[2]), hoist = True, display_icon = None, mentionable = False)

            for member in member_list:
                await member.add_roles(role)
                
            permissions_everyone = discord.PermissionOverwrite()
            permissions_everyone.read_messages = False
            permissions_everyone.connect = False
            permissions_team = discord.PermissionOverwrite()
            permissions_team.read_messages = True
            permissions_everyone.connect = True

            text_category = discord.utils.get(interaction.guild.categories, id = settings.text_category_id)
            voice_category = discord.utils.get(interaction.guild.categories, id = settings.voice_category_id)

            text_channel = await text_category.create_text_channel(team_name)
            
            await asyncio.sleep(1)
            
            await text_channel.set_permissions(interaction.guild.default_role, overwrite = permissions_everyone)
            await text_channel.set_permissions(role, overwrite = permissions_team)
            
            await asyncio.sleep(1)
            
            voice_channel = await voice_category.create_voice_channel(team_name)
            
            await asyncio.sleep(1)
            
            await voice_channel.set_permissions(interaction.guild.default_role, overwrite = permissions_everyone)
            await voice_channel.set_permissions(role, overwrite = permissions_team)
            
            await asyncio.sleep(1)
            
            team_id = utils.db.last_team_id() + 1
            team = Team(team_id, role.id, interaction.guild_id, member_list, team_name, member_1.id, text_channel.id, voice_channel.id)
            utils.db.add_team(team)
            
            teams_channel = discord.utils.get(interaction.guild.channels, id = settings.teams_channel_id)
            team_embed = utils.Embed.team(team, color)
            await teams_channel.send(embed = team_embed)
        except Exception as error:
            embed = utils.Embed.error(error.__str__())
            await interaction.edit_original_response(embed = embed)
        else:
            embed = utils.Embed.success(f"Successfully added team **{team_name}**!")
            await interaction.edit_original_response(embed = embed)

    @add.error
    async def on_cooldown_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            embed = utils.Embed.error(CommandLimitReached().__str__())
            await interaction.response.send_message(embed = embed, ephemeral = True)
            
    @app_commands.checks.cooldown(1, 1, key = lambda i: (i.guild.id))
    @app_commands.describe(role = "Select team's role.")
    @app_commands.command(
        name = "delete", 
        description = "Deletes a team from Database"
    )
    async def delete(
        self,
        interaction: discord.Interaction,
        role: discord.Role
    ):
        await interaction.response.send_message(embed = utils.Embed.loading())
                
        try:
            if not interaction.user.guild_permissions.administrator:
                raise NoAdmin()
            
            if not utils.db.get_settings(interaction.guild_id):
                raise BotNotSetUp()
                
            team = utils.db.get_team(role.id, interaction.guild_id)
            
            if team == None:
                raise TeamNotFound()
            
            role = discord.utils.get(interaction.guild.roles, id = team.role_id)
            if role != None:
                await role.delete()
            
            await asyncio.sleep(1)
            
            text_channel = discord.utils.get(interaction.guild.channels, id = team.text_channel_id)
            if text_channel != None:
                await text_channel.delete()
            
            await asyncio.sleep(1)
            
            voice_channel = discord.utils.get(interaction.guild.channels, id = team.voice_channel_id)
            if voice_channel != None:
                await voice_channel.delete()
            
            await asyncio.sleep(1)
                
            team_name = utils.db.remove_team(role.id, interaction.guild_id)
        except Exception as error:
            embed = utils.Embed.error(error.__str__())
            await interaction.edit_original_response(embed = embed)
        else:
            embed = utils.Embed.success(f"Successfully removed team **{team_name}**!")
            await interaction.edit_original_response(embed = embed)

    @delete.error
    async def on_cooldown_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            embed = utils.Embed.error(CommandLimitReached().__str__())
            await interaction.response.send_message(embed = embed, ephemeral = True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(team(bot))