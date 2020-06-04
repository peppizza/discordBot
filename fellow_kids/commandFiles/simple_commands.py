import json
import discord
import random
import asyncio
import os

from discord.ext import commands
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

class SimpleCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        with open("{}/assets/images.json".format(THIS_FOLDER), 'r') as in_file:
            data = json.load(in_file)
            self.tf2images = data['tf2images']
            self.smuganime = data['smuganime']

    @commands.command()
    async def server(self, ctx):
        await ctx.send('https://cache.gametracker.com/server_info/168.62.169.84:27015/b_350_20_692108_381007_ffffff_000000.png')

    @commands.command(help='how do you do fellow kids')
    async def kids(self, ctx):
        await ctx.send('https://www.youtube.com/watch?v=bI2PdskxE_s')

    @commands.command(help='pootis')
    async def pootis(self, ctx):
        await ctx.send('pootis')

    @commands.command(help='jesus')
    async def jesus(self, ctx):
        await ctx.send('https://www.you-need-jesus.com/')

    @commands.command(help='your mom be a hoe')
    async def momsahoe(self, ctx):
        await ctx.send('https://www.youtube.com/watch?v=iYx_aGlmyc4')

    @commands.command(help='heyayayaya')
    async def hey(self, ctx):
        await ctx.send('https://www.youtube.com/watch?v=ZZ5LpwO-An4&t=13s')

    @commands.command(help='shrek')
    async def shrek(self, ctx):
        await ctx.send('https://www.youtube.com/watch?v=psFzJv8g6jc')

    @commands.command(help='hamburger')
    async def hamburger(self, ctx):
        await ctx.send('https://www.youtube.com/watch?v=qIJ-lchwqVA')

    @commands.command(help='selects random tf2 image')
    async def tf2image(self, ctx):
        await ctx.send(random.choice(self.tf2images))

    @commands.command(help='no u')
    async def nou(self, ctx):
        await ctx.send('https://cdn.discordapp.com/attachments/684474004563689539/685130037585772552/deepfried_1583418116265.png')

    @commands.command(help='gay')
    async def gay(self, ctx):
        await ctx.send('https://www.villagevoice.com/wp-content/uploads/2011/02/thatsgay.png')

    @commands.command(help='kool aid man')
    async def ohyeah(self, ctx):
        await ctx.send('https://i.pinimg.com/736x/e2/d2/4a/e2d24a8338a81191c59b928c2cbeedcf.jpg')

    @commands.command(help='deep')
    async def deep(self, ctx):
        await ctx.send('https://preview.redd.it/she0nt0g5b131.jpg?auto=webp&s=e77d77c2bf39d54d9cb89457eee61220d5700df4')

    @commands.command(help='demoman laughing')
    async def laugh(self, ctx):
        await ctx.send('https://i.redd.it/l32xlpu8vad31.jpg')

    @commands.command(help='bruh sound effect #2')
    async def bruh(self, ctx):
        await ctx.send('https://www.youtube.com/watch?v=2ZIpFytCSVc')

    @commands.command(help='get vectored')
    async def vector(self, ctx):
        await ctx.send('https://cdn.discordapp.com/attachments/685262422252191781/685591126442377266/download.jpg')

    @commands.command(help='gonk image')
    async def gonk(self, ctx):


        discord.Embed().set_image(url = 'https://cdn.discordapp.com/attachments/685262422252191781/685621651970326545/unknown.png')

        await ctx.send(embed = discord.Embed().set_image(url = 'https://cdn.discordapp.com/attachments/685262422252191781/685621651970326545/unknown.png'))
        await ctx.send('https://cdn.discordapp.com/attachments/685262422252191781/685621651970326545/unknown.png')

    @commands.command(help='prints smug anime girl')
    async def smug(self, ctx):
        await ctx.send(random.choice(self.smuganime))

    @commands.command(help='demoman tf2')
    async def didntseethat(self, ctx):
        await ctx.send('https://cdn.discordapp.com/attachments/685262422252191781/689161554318721042/maxresdefault.jpg')

    @commands.command()
    async def spycrab(self, ctx):
        await ctx.send('https://i.imgur.com/ufzaw81.png')

    @commands.command()
    async def whygay(self, ctx):
        await ctx.send('https://cdn.discordapp.com/attachments/697102775959552052/704357844572438598/images.jpg')

    @commands.command()
    async def monke(self, ctx):
        await ctx.send('https://i.redd.it/97vk2gz7zvl41.jpg')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.count != 1: return
        message = reaction.message
        emoji = reaction.emoji
        await asyncio.sleep(random.randint(1, 3))
        await message.add_reaction(emoji)

    @commands.command()
    async def money(self, ctx):
        await ctx.send('https://cdn.discordapp.com/attachments/696786725053399092/717430238941937764/1480273770_spy1.gif')