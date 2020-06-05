import os
import json
import discord
import asyncio

from discord.ext import commands
from commandFiles import THIS_FOLDER, ROLE_ADMINISTRATOR
level = os.path.join(THIS_FOLDER, 'level.json')

class Leveling(commands.Cog):
    def __init__(self, bot):
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

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        currentlevel = ''
        user = str(message.author.id)
        channel = message.channel
        with open(level, 'r') as read_file:
            data = json.load(read_file)
        if user in data:
            if currentlevel == '':
                data[user] = [data[user][0] + 1, data[user][1]]
            else:
                data[user] = [data[user][0] + 1, currentlevel]
        else:
            data[user] = [1, '']
        
        if str(data[user][0]) in self.levels:
            currentlevel = self.levels.get(str(data[user][0]))
            data[user][1] = currentlevel
            embed = discord.Embed(title="{} has leveled up".format(message.author), color=0x00ff00)
            embed.set_image(url='https://france-amerique.com/wp-content/uploads/2018/01/flute-e1516288055295.jpg')
            embed.add_field(name='messages sent:', value=data[user][0])
            embed.add_field(name='level reached:', value=currentlevel)
            await channel.send(embed=embed)

        with open(level, 'w') as write_file:
            json.dump(data, write_file)

    @commands.command()
    async def level(self, ctx):

        user = str(ctx.author.id)
        
        with open(level, 'r') as read_file:
            data = json.load(read_file)
        
        if user in data:
            if data[user][1] == '':
                level = 'None'
            else:
                level = data[user][1]
            embed = discord.Embed(title='Level')
            embed.add_field(name='messages sent:', value=data[user][0])
            embed.add_field(name='current level:', value=level)
            await ctx.send(embed=embed)
        else:
            await ctx.send('{} has not sent any messages yet'.format(ctx.author.mention))

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
            open(level, 'w').write('{}')
            await ctx.send('Erased levels')
        
    @commands.command()
    @commands.has_role(ROLE_ADMINISTRATOR)
    async def cancel(self, ctx):
        self.erase = False
        await ctx.send('Rocket launch canceled')

    @commands.command()
    @commands.has_role(ROLE_ADMINISTRATOR)
    async def count(self, ctx, member: discord.Member, level: int, custom=''):
        with open(level, 'r') as in_file:
            data = json.load(in_file)

        user = str(member.id)
        if user in data:
            data[user][0] = level
            if custom != '':
                data[user][1] = custom

        with open(level, 'w') as out_file:
            json.dump(data, out_file)

    @count.error
    async def count_on_error(self, ctx, error):
        await ctx.send(error)