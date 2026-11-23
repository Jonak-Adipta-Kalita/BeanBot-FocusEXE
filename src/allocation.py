import main
import discord

from discord.ext import commands


class Allocation(commands.Cog):
    def __init__(self, bot: main.DiscordBot):
        self.bot = bot

    def random_allocation():
        pass

    def allocate_current_members():
        pass

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = member.guild.system_channel
        if channel:
            await channel.send(f"Welcome {member.mention}!")


async def setup(bot: main.DiscordBot):
    await bot.add_cog(Allocation(bot))
