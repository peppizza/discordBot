import discord
import asyncio
import sqlite3

from discord.ext import commands, tasks
from .constants import THIS_FOLDER, ROLE_ADMINISTRATOR

class Leveling(commands.Cog):
    def __init__(self, bot):
        """The leveling system."""
        self.bot = bot
        self.levels = {
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
        self.db = sqlite3.connect('levels.db')
        self.cursor = self.db.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS levels(
                id INTEGER PRIMARY KEY,
                messages INTEGER
            )
        """)
        
        self.cursor.execute('SELECT * FROM levels')
        rows = self.cursor.fetchall()
        self.cachedLevels = dict(rows)
        self.calculateLevels()
        self.saveLoop.start()

    def calculateLevels(self):
        for memberId in self.cachedLevels.keys():
            level = self.cachedLevels[memberId]
            levelName = self.levels.get(level, self.levels[min(self.levels.keys(), key=lambda k: abs(k-level))])
            self.cachedLevels[memberId] = [level, levelName]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: return
        if self.cachedLevels.get(message.author.id) is None:
            self.cachedLevels[message.author.id] = [0, 'None']
        self.cachedLevels[message.author.id] = [self.cachedLevels[message.author.id][0] + 1, self.cachedLevels[message.author.id][1]]

        if self.cachedLevels[message.author.id][0] in self.levels:
            currentlevel = self.levels.get(self.cachedLevels[message.author.id][0])
            embed = discord.Embed(title=f'{message.author} has leveled up', color=0x00ff00)
            embed.set_image(url='https://france-amerique.com/wp-content/uploads/2018/01/flute-e1516288055295.jpg')
            embed.add_field(name='messages sent:', value=self.cachedLevels[message.author.id][0])
            embed.add_field(name='level reached:', value=currentlevel)
            await message.channel.send(embed=embed)
            self.cachedLevels[message.author.id][1] = currentlevel

    @commands.command()
    async def level(self, ctx, member: discord.Member = None):
        embed = discord.Embed(title="Level")
        if member is None:
            if self.cachedLevels.get(ctx.author.id, None) is not None:
                embed.add_field(name="messages sent", value=self.cachedLevels[ctx.author.id][0])
                embed.add_field(name="current level", value=self.cachedLevels[ctx.author.id][1])
            else:
                embed.description = "you have not sent any messages yet"
                embed.color = 0xff0000
        else:
            if self.cachedLevels.get(member.id, None) is not None:
                embed.add_field(name="messages sent", value=self.cachedLevels[member.id][0])
                embed.add_field(name="current level", value=self.cachedLevels[member.id][1])
            else:
                embed.description = "this user has not sent any messages yet"
                embed.color = 0xff0000
        await ctx.send(embed=embed)

    @tasks.loop(minutes=5.0)
    async def saveLoop(self):
        data = self.saveDB()
        self.cursor.executemany('REPLACE INTO levels(id,messages) VALUES(?,?)', data)
        self.db.commit()

    @commands.command()
    @commands.is_owner()
    async def save(self, ctx):
        data = self.saveDB()

        self.cursor.executemany('REPLACE INTO levels(id,messages) VALUES(?,?)', data)
        self.db.commit()

    @commands.command()
    @commands.has_role(ROLE_ADMINISTRATOR)
    async def reset(self, ctx):
        self.cursor.execute('DELETE FROM levels')
        self.erase = True
        await ctx.send('YOU\'VE LAUNCHED THE ROCKET')
        for x in range(5, 0, -1):
            await asyncio.sleep(1)
            if self.erase == False:
                self.db.rollback()
                return
            await ctx.send(x)
        if self.erase == True:
            await asyncio.sleep(1)
            self.cachedLevels = {}
            self.db.commit()
            await ctx.send('levels erased')
        else:
            self.db.rollback()
        
    @commands.command()
    @commands.has_role(ROLE_ADMINISTRATOR)
    async def cancel(self, ctx):
        self.erase = False
        await ctx.send('Rocket launch canceled')

    def saveDB(self):
        data = []
        for key in list(self.cachedLevels.keys()):
            data.append((key, self.cachedLevels[key][0]))

        return data

    def cog_unload(self):
        self.saveLoop.cancel()
        data = self.saveDB()
        self.cursor.executemany('REPLACE INTO levels(id,messages) VALUES(?,?)', data)
        self.db.commit()

def setup(bot):
    bot.add_cog(Leveling(bot))