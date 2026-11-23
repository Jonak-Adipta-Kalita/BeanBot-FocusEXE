import discord

from discord.ext import commands
from discord import app_commands


class DiscordBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="$",
            intents=discord.Intents.all(),
            help_command=None,
            allowed_contexts=app_commands.AppCommandContext(
                guild=True
            ),
            allowed_installs=app_commands.AppInstallationType(guild=True),
        )

    async def on_connect(self):
        print("Bot Connected!")

    async def on_disconnect(self):
        print("Bot is Disconnected!!")
