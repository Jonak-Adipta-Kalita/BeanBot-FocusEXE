import main
import random
import discord
import credentials

from discord.ext import commands

ROLES = {
    "Kidney Bean": 1574074600101511321,
    "Coffee Bean": 1574074669043163239,
    "Jelly Bean": 1574074707005939825,
    "Soy Bean": 1574074811976523796
}


class Allocation(commands.Cog):
    def __init__(self, bot: main.DiscordBot):
        self.bot = bot

    def random_allocation(self):
        pass

    def allocate_current_members():
        pass

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        # TODO: Not random, be strategic on how many each has
        random_role = random.choice(ROLES.keys())
        role = member.guild.get_role(ROLES[random_role])

        if role:
            await member.add_roles(role)
            # TODO: Add User to DB
        else:
            channel = member.guild.get_channel_or_thread(
                credentials.SERVER_CHANNEL_ID)

            embed = discord.Embed(
                title="Error in on_member_join of Allocation",
                color=discord.Color.blue())
            embed.description = f"No Role found for: {random_role}"

            channel.send(embed=embed)


async def setup(bot: main.DiscordBot):
    await bot.add_cog(Allocation(bot))
