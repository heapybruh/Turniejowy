import utils
from utils import NoAdmin, TooSmallTeam, TeamNotFound, CommandLimitReached, BotNotSetUp, WrongRoleColor
from models import Team
import discord
from discord import app_commands
from discord.ext import commands
from PIL import ImageColor

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
        member_5 = "Select user."
    )
    @app_commands.command(
        name = "add", 
        description = "Adds a team (max 5-stacked, minimum 2-stacked) to Database"
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
        member_5: discord.Member = None
    ):
        message: discord.Message | None = None
        
        try:
            if not interaction.user.guild_permissions.administrator:
                raise NoAdmin()

            settings = utils.db.get_settings(interaction.guild_id)
            if not settings:
                raise BotNotSetUp()

            member_list = list(set([x for x in [member_1, member_2, member_3, member_4, member_5] if x is not None]))

            if len(member_list) < 2:
                raise TooSmallTeam()
            
            if len(role_color) != 7:
                raise WrongRoleColor()
            
            await interaction.response.send_message(embed = utils.Embed.loading(), ephemeral = True)
            
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
            await text_channel.set_permissions(interaction.guild.default_role, overwrite = permissions_everyone)
            await text_channel.set_permissions(role, overwrite = permissions_team)
            voice_channel = await voice_category.create_voice_channel(team_name)
            await voice_channel.set_permissions(interaction.guild.default_role, overwrite = permissions_everyone)
            await voice_channel.set_permissions(role, overwrite = permissions_team)

            team_id = utils.db.last_team_id() + 1
            team = Team(team_id, role.id, interaction.guild_id, member_list, team_name, member_1.id)
            utils.db.add_team(team)
            
            embed = utils.Embed.success(f"Successfully added team **{team_name}**!")
            await interaction.edit_original_response(embed = embed)
        except Exception as error:
            embed = utils.Embed.error(error.__str__())
            await interaction.edit_original_response(embed = embed) if message else await interaction.response.send_message(embed = embed, ephemeral = True)

    @add.error
    async def on_cooldown_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            embed = utils.Embed.error(CommandLimitReached().__str__())
            await interaction.response.send_message(embed = embed, ephemeral = True)
            
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
                raise NoAdmin()
            
            if not utils.db.get_settings(interaction.guild_id):
                raise BotNotSetUp()
                
            team = utils.db.get_team(team_id, interaction.guild_id)
            
            if team == None:
                raise TeamNotFound()
                
            team_name = utils.db.remove_team(team_id)
            
            embed = utils.Embed.success(f"Successfully removed team **{team_name}**!")
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
    await bot.add_cog(team(bot))