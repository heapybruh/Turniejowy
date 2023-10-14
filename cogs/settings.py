import utils
from utils import CommandLimitReached, NoAdmin, BotNotSetUp
from models import Settings
import discord
from discord import app_commands
from discord.ext import commands

class settings(commands.GroupCog, name = "settings"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.checks.cooldown(1, 1, key = lambda i: (i.guild.id))
    @app_commands.command(
        name = "get", 
        description = "Returns bot's settings"
    )
    async def get(
        self,
        interaction: discord.Interaction
    ):
        try:
            if not interaction.user.guild_permissions.administrator:
                raise NoAdmin()
            
            settings = utils.db.get_settings(interaction.guild_id)
            if not settings:
                raise BotNotSetUp()
            
            embed = utils.Embed.settings(interaction.guild_id)
            await interaction.response.send_message(embed = embed)
        except Exception as error:
            embed = utils.Embed.error(error.__str__())
            await interaction.response.send_message(embed = embed, ephemeral = True)

    @get.error
    async def on_cooldown_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            embed = utils.Embed.error(CommandLimitReached().__str__())
            await interaction.response.send_message(embed = embed, ephemeral = True)
            
    @app_commands.checks.cooldown(1, 1, key = lambda i: (i.guild.id))
    @app_commands.describe(
        text_category = "Select category for teams' text channels.",
        voice_category = "Select category for teams' voice channels."
    )
    @app_commands.command(
        name = "setup", 
        description = "Creates/Updates settings"
    )
    async def setup(
        self,
        interaction: discord.Interaction,
        text_category: discord.CategoryChannel,
        voice_category: discord.CategoryChannel,
        teams_channel: discord.TextChannel
    ):
        try:
            if not interaction.user.guild_permissions.administrator:
                raise NoAdmin()
            
            settings = utils.db.get_settings(interaction.guild_id)
            if not settings:
                utils.db.add_settings(Settings(interaction.guild_id, text_category.id, voice_category.id, teams_channel.id))                
                embed = utils.Embed.success("Successfully created settings.")
            else:
                utils.db.update_settings(Settings(interaction.guild_id, text_category.id, voice_category.id, teams_channel.id))
                embed = utils.Embed.success("Successfully updated settings.")
                
            await interaction.response.send_message(embed = embed)
        except Exception as error:
            embed = utils.Embed.error(error.__str__())
            await interaction.response.send_message(embed = embed, ephemeral = True)

    @setup.error
    async def on_cooldown_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            embed = utils.Embed.error(CommandLimitReached().__str__())
            await interaction.response.send_message(embed = embed, ephemeral = True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(settings(bot))