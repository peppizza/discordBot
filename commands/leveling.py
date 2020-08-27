import discord
import asyncio
import asyncpg

from discord.ext import commands, tasks
from .constants import ROLE_ADMINISTRATOR


class Leveling(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        """The leveling system."""
        self.bot = bot
        self.levels = {
            0: "None",
            10: "Unremarkable",
            25: "Scarcely Lethal",
            45: "Mildly Menacing",
            70: "Somewhat Threatening",
            100: "Uncharitable",
            135: "Notably Dangerous",
            175: "Sufficiently Lethal",
            225: "Truly Feared",
            275: "Spectacularly Lethal",
            350: "Gore-Spattered",
            500: "Wicked Nasty",
            750: "Positively Inhumane",
            999: "Totally Ordinary",
            1000: "Face-Melting",
            1500: "Rage-Inducing",
            2500: "Server-Clearing",
            5000: "Epic",
            7500: "Legendary",
            7616: "Australian",
            8500: "Hale's Own"
        }
        self.erase = False
        self.cachedLevels = {}
        self.bot.loop.create_task(self.async_init())

    async def async_init(self):
        await self.bot.wait_until_ready()
        async with self.bot.pool.acquire() as connection:
            connection: asyncpg.Connection
            async with connection.transaction():
                rows = await connection.fetch('SELECT * FROM levels')
                cachedLevels = {}
                for i in rows:
                    cachedLevels[i[0]] = i[1:]

                self.cachedLevels = cachedLevels
                self.saveLoop.start()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if self.cachedLevels.get(message.author.id) is None:
            self.cachedLevels[message.author.id] = [0, 'None']
        self.cachedLevels[message.author.id] = [
            self.cachedLevels[message.author.id][0] + 1, self.cachedLevels[message.author.id][1]]

        if self.cachedLevels[message.author.id][0] in self.levels:
            currentlevel = self.levels.get(
                self.cachedLevels[message.author.id][0])
            embed = discord.Embed(
                title=f'{message.author} has leveled up', color=0x00ff00)
            embed.set_thumbnail(
                url='https://france-amerique.com/wp-content/uploads/2018/01/flute-e1516288055295.jpg')
            embed.add_field(name='messages sent:',
                            value=self.cachedLevels[message.author.id][0])
            embed.add_field(name='level reached:', value=currentlevel)
            await message.channel.send(embed=embed)
            self.cachedLevels[message.author.id][1] = currentlevel

    @commands.command()
    async def level(self, ctx, member: discord.Member = None):
        embed = discord.Embed(title="Level")
        if member is None:
            if self.cachedLevels.get(ctx.author.id, None) is not None:
                embed.add_field(name="messages sent",
                                value=self.cachedLevels[ctx.author.id][0])
                embed.add_field(name="current level",
                                value=self.cachedLevels[ctx.author.id][1])
            else:
                embed.description = "you have not sent any messages yet"
                embed.color = 0xff0000
        else:
            if self.cachedLevels.get(member.id, None) is not None:
                embed.add_field(name="messages sent",
                                value=self.cachedLevels[member.id][0])
                embed.add_field(name="current level",
                                value=self.cachedLevels[member.id][1])
            else:
                embed.description = "this user has not sent any messages yet"
                embed.color = 0xff0000
        await ctx.send(embed=embed)

    @tasks.loop(minutes=5.0)
    async def saveLoop(self):
        data = self.saveDB()

        await self.save_to_db(data)

    @commands.command()
    @commands.is_owner()
    async def save(self, ctx):
        data = self.saveDB()

        await self.save_to_db(data)

    @commands.command()
    @commands.has_role(ROLE_ADMINISTRATOR)
    async def reset(self, ctx):
        self.erase = True
        await ctx.send('YOU\'VE LAUNCHED THE ROCKET')
        for x in range(5, 0, -1):
            await asyncio.sleep(1)
            if self.erase == False:
                await self.db.rollback()
                return
            await ctx.send(x)
        if self.erase == True:
            await asyncio.sleep(1)
            self.cachedLevels = {}
            async with self.bot.pool.acquire() as connection:
                connection: asyncpg.Connection
                async with connection.transaction():
                    await connection.execute('TRUNCATE levels')
            await ctx.send('levels erased')

    @commands.command()
    @commands.has_role(ROLE_ADMINISTRATOR)
    async def cancel(self, ctx):
        self.erase = False
        await ctx.send('Rocket launch canceled')

    def saveDB(self):
        data = []
        for key in list(self.cachedLevels.keys()):
            data.append(
                (key, self.cachedLevels[key][0], self.cachedLevels[key][1]))

        return data

    def cog_unload(self):
        self.saveLoop.cancel()
        data = self.saveDB()
        self.bot.loop.create_task(self.save_to_db(data))

    async def save_to_db(self, data):
        async with self.bot.pool.acquire() as connection:
            connection: asyncpg.Connection
            async with connection.transaction():
                await connection.executemany('''INSERT INTO levels(id,messages,level) VALUES ($1, $2, $3)
                                             ON CONFLICT (id) DO UPDATE
                                                SET id = EXCLUDED.id,
                                                messages = EXCLUDED.messages,
                                                level = EXCLUDED.level''', data)


def setup(bot):
    bot.add_cog(Leveling(bot))
