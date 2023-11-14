import utils
from utils import NoAdmin, TooSmallTeam, TeamNotFound, CommandLimitReached, BotNotSetUp, WrongRoleColor, Team, UserAlreadyInTeam, Member
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
        role_color = "Enter color in HEX. (example: #ffffff)",
        team_name = "Enter team name.",
        member_1 = "Select team owner.",
        member_2 = "Select team member.",
        member_3 = "Select team member.",
        member_4 = "Select team member.",
        member_5 = "Select team member.",
        reserve_member_1 = "Select team reserve member.",
        reserve_member_2 = "Select team reserve member."
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

            settings = utils.db.get_settings(guild = interaction.guild_id)
            if not settings:
                raise BotNotSetUp()

            member_list = [
                Member(
                    discord = member.id, 
                    guild = member.guild.id
                ) for member in [
                    member_1, 
                    member_2, 
                    member_3, 
                    member_4, 
                    member_5, 
                    reserve_member_1, 
                    reserve_member_2
                ] if member is not None
            ]
            member_list = list(set(member_list))

            if len(member_list) < 2:
                raise TooSmallTeam()
            
            if len(role_color) != 7:
                raise WrongRoleColor()
            
            if settings.team_owner_role != 0:
                owner_role = discord.utils.get(interaction.guild.roles, id = settings.team_owner_role)
                if not owner_role:
                    raise BotNotSetUp()
            
                await member_1.add_roles(owner_role)

            for member in member_list:
                member_team = utils.db.get_member_team(Member(discord = member.id, guild = member.guild))
                if member_team:
                    raise UserAlreadyInTeam()
            
            color = ImageColor.getrgb(role_color)
            role_color = discord.Colour.from_rgb(r = color[0], g = color[1], b = color[2])

            role = await interaction.guild.create_role(
                name = team_name, 
                permissions = discord.Permissions.none(), 
                colour = role_color, 
                hoist = True, 
                display_icon = None, 
                mentionable = False
            )

            for member in member_list:
                member_discord = await interaction.guild.fetch_member(member.discord)
                await member_discord.add_roles(role)
                
            permissions_everyone = discord.PermissionOverwrite()
            permissions_everyone.read_messages = False
            permissions_team = discord.PermissionOverwrite()
            permissions_team.read_messages = True

            text_category = discord.utils.get(interaction.guild.categories, id = settings.text_category)
            voice_category = discord.utils.get(interaction.guild.categories, id = settings.voice_category)

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
            
            team = Team(
                role = role.id, 
                guild = interaction.guild_id, 
                members = member_list, 
                name = team_name, 
                owner = member_1.id, 
                text_channel = text_channel.id, 
                voice_channel = voice_channel.id
            )
            
            team_list = discord.utils.get(interaction.guild.channels, id = settings.team_list_channel)
            team_embed = utils.Embed.team(team, role_color)
            message = await team_list.send(embed = team_embed)
            team.message = message.id
            
            utils.db.add_team(team)
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
    @app_commands.describe(role = "Select team.")
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
            
            settings = utils.db.get_settings(interaction.guild_id)
            if not settings:
                raise BotNotSetUp()
                
            team = utils.db.get_team(role.id, interaction.guild_id)
            
            if not team:
                raise TeamNotFound()
            
            role = discord.utils.get(interaction.guild.roles, id = team.role)
            if role:
                await role.delete()
                await asyncio.sleep(1)
                
            owner = discord.utils.get(interaction.guild.members, id = team.owner)
            if owner:
                owner_role = discord.utils.get(interaction.guild.roles, id = settings.team_owner_role)
                if owner_role in owner.roles:
                    await owner.remove_roles(owner_role)
            
            text_channel = discord.utils.get(interaction.guild.channels, id = team.text_channel)
            if text_channel:
                await text_channel.delete()
                await asyncio.sleep(1)
            
            voice_channel = discord.utils.get(interaction.guild.channels, id = team.voice_channel)
            if voice_channel:
                await voice_channel.delete()
                await asyncio.sleep(1)
            
            teams_channel = discord.utils.get(interaction.guild.channels, id = settings.team_list_channel)
            if teams_channel:
                try:
                    message = await teams_channel.fetch_message(team.message)
                    await message.delete()
                except:
                    pass
                else:
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