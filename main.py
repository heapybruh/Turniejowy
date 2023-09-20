import tools
import discord
from discord.ext import commands, tasks
import os

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")

    class Bot(commands.Bot):
        def __init__(self):
            intents = discord.Intents.default()
            intents.presences = True
            intents.members = True

            super().__init__(
                command_prefix = "/", 
                intents = intents)

        async def setup_hook(self):
            for file in tools.Cogs.get():
                if file.is_dir():
                    continue
             
                extension = f"cogs.{file.stem}"
                await self.load_extension(extension)
                print(f"[✓] Loaded {extension}")

        @tasks.loop(minutes = 5)
        async def rich_presence(self):
            await self.change_presence(activity = discord.Activity(type = discord.ActivityType.playing, name = "Helping with Discord Tournaments..."))

        async def on_ready(self):
            await self.tree.sync()
            
            tools.db = tools.Database(self)

            try:
                self.rich_presence.start()
            except:
                print("[⚠] Couldn't start rich presence!")

            print(f"[✓] Discord.py v{discord.__version__} → {self.user} ({self.user.id})")

    config = tools.Config()
    bot = Bot()
    bot.run(config.token, log_handler = None)