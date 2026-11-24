import main
import asyncio
import discord
import credentials

from discord.ext import commands

ROLES = {
    "Kidney Bean": 1574074600101511321,
    "Coffee Bean": 1574074669043163239,
    "Jelly Bean": 1574074707005939825,
    "Soy Bean": 1574074811976523796,
}


class Allocation(commands.Cog):
    def __init__(self, bot: main.DiscordBot):
        self.bot = bot
        self.lock = asyncio.Lock()
        self.guild_id = credentials.SERVER_ID
        self.allocations: dict[int, int] = {}
        self.counts: dict[int, int] = {}
        self._sync_task: asyncio.Task | None = None

    async def cog_load(self):
        self.allocations = self.bot.db.get_allocations()
        self.counts = {rid: 0 for rid in ROLES.values()}
        for rid in self.allocations.values():
            if rid in self.counts:
                self.counts[rid] += 1

        self._sync_task = asyncio.create_task(self.sync_members())

    async def cog_unload(self):
        if self._sync_task:
            self._sync_task.cancel()

    async def log_error(self, guild: discord.Guild, message: str):
        print(message)
        channel = guild.get_channel_or_thread(credentials.SERVER_CHANNEL_ID)
        if channel is None:
            return
        embed = discord.Embed(
            title="Error in Allocation",
            description=message,
            color=discord.Color.red(),
        )
        try:
            await channel.send(embed=embed)
        except discord.HTTPException:
            pass

    def least_filled_role(self) -> int:
        return min(self.counts, key=self.counts.get)

    async def ensure_role(self, member: discord.Member):
        if member.bot:
            return

        async with self.lock:
            role_id = self.allocations.get(member.id)

            if role_id is None:
                existing = next(
                    (r.id for r in member.roles if r.id in self.counts), None
                )
                role_id = existing or self.least_filled_role()

                self.allocations[member.id] = role_id
                self.counts[role_id] += 1
                self.bot.db.add_allocation(member.id, role_id)

            role = member.guild.get_role(role_id)
            if role is None:
                await self.log_error(member.guild, f"No Role found for ID: {role_id}")
                return

            if role not in member.roles:
                try:
                    await member.add_roles(role, reason="Role allocation")
                except (discord.Forbidden, discord.HTTPException) as e:
                    await self.log_error(member.guild, f"Failed to add {
                        role.name} to {member}: {e}")

    async def sync_members(self):
        await self.bot.wait_until_ready()

        guild = self.bot.get_guild(self.guild_id)
        if guild is None:
            print(f"Guild {self.guild_id} not found!")
            return

        missing = [name for name, rid in ROLES.items()
                                                     if guild.get_role(rid) is None]
        if missing:
            await self.log_error(
                guild, f"Missing roles in server: {', '.join(missing)}"
            )
            return

        for member in list(guild.members):
            await self.ensure_role(member)

        print(f"Allocation sync done. Counts: {self.counts}")

  @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.guild.id != self.guild_id:
            return
        await self.ensure_role(member)


async def setup(bot: main.DiscordBot):
    await bot.add_cog(Allocation(bot))
