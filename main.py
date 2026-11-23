import credentials
import discord

from discord.ext import commands
from discord import app_commands

from src.db import Database


class DiscordBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True

        super().__init__(
            command_prefix=".",
            intents=intents,
            help_command=None,
            allowed_contexts=app_commands.AppCommandContext(guild=True),
            allowed_installs=app_commands.AppInstallationType(guild=True),
        )

        self.db = Database()

    async def setup_hook(self):
        await self.load_extension("src.allocation")

    async def on_connect(self):
        print("Bot Connected!")

    async def on_disconnect(self):
        print("Bot is Disconnected!!")


if __name__ == "__main__":
    try:
        bot = DiscordBot()
        bot.run(credentials.TOKEN)
    except KeyboardInterrupt:
        print("Bot Exited!!")
