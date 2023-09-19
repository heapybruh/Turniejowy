import tools
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
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message("You don't have **__Administrator__** permission!", ephemeral = True)

            embed = tools.Embed.user(user, interaction.guild_id)
            await interaction.response.send_message(embed = embed)
        except Exception as error:
            await interaction.response.send_message(f"Error: {error}", ephemeral = True)

    @check.error
    async def on_cooldown_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message("This guild is limited to use this command once per second! Try again in 1s...", ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(user(bot))