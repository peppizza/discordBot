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
            "10": "Unremarkable",
            "25": "Scarcely Lethal",
            "45": "Mildly Menacing",
            "70": "Somewhat Threatening",
            "100": "Uncharitable",
            "135": "Notably Dangerous",
            "175": "Sufficiently Lethal",
            "225": "Truly Feared",
            "275": "Spectacularly Lethal",
            "350": "Gore-Spattered",
            "500": "Wicked Nasty",
            "750": "Positively Inhumane",
            "999": "Totally Ordinary",
            "1000": "Face-Melting",
            "1500": "Rage-Inducing",
            "2500": "Server-Clearing",
            "5000": "Epic",
            "7500": "Legendary",
            "7616": "Australian",
            "8500": "Hale's Own"
        }
        self.erase = False
        self.cachedLevels = {}
        self.db = sqlite3.connect('levels.db')
        self.cursor = self.db.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS levels(
                id INTEGER,
                level INTEGER
            )
        """)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: return
        if self.cachedLevels.get(message.author.id) is None:
            self.cachedLevels[message.author.id] = 0
        self.cachedLevels[message.author.id] = self.cachedLevels.get(message.author.id) + 1

    @commands.command()
    async def level(self, ctx):
        embed = discord.Embed(title="Level")
        embed.add_field(name="current level", value=self.cachedLevels.get(ctx.author.id))
        await ctx.send(embed=embed)

    @tasks.loop(minutes=5.0)
    async def saveLoop(self):
        self.cursor.execute('INSERT INTO levels VALUES(?,?)', (self.cachedLevels.keys(), self.cachedLevels.values()))

    @commands.command()
    @commands.is_owner()
    async def save(self, ctx):
        levels = [
            list(self.cachedLevels.keys()),
            list(self.cachedLevels.values())
        ]
        print(levels)
        try:
            self.cursor.executemany('INSERT OR REPLACE INTO levels VALUES(?, ?)', levels)
        except sqlite3.ProgrammingError:
            pass

        self.db.commit()

    @commands.command()
    @commands.has_role(ROLE_ADMINISTRATOR)
    async def reset(self, ctx):
        self.erase = True
        await ctx.send('YOU\'VE LAUNCHED THE ROCKET')
        for x in range(5, 0, -1):
            await asyncio.sleep(1)
            if self.erase == False:
                return
            await ctx.send(x)
        if self.erase == True:
            await asyncio.sleep(1)
            # TODO: erase all data with sql
        
    @commands.command()
    @commands.has_role(ROLE_ADMINISTRATOR)
    async def cancel(self, ctx):
        self.erase = False
        await ctx.send('Rocket launch canceled')

def setup(bot):
    bot.add_cog(Leveling(bot))