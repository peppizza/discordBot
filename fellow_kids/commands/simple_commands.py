import json
import random
import asyncio

from discord.ext import commands
from .constants import THIS_FOLDER

class SimpleCommands(commands.Cog):

    def __init__(self, bot: commands.AutoShardedBot):
        """Simple commands that take in no arguments."""
        self.bot = bot
        with open("{}/assets/images.json".format(THIS_FOLDER), 'r') as in_file:
            data = json.load(in_file)
            self.tf2images = data['tf2images']
            self.smuganime = data['smuganime']

    @commands.command(help='how do you do fellow kids')
    async def kids(self, ctx):
        await ctx.send('https://www.youtube.com/watch?v=bI2PdskxE_s')

    @commands.command(help='Selects random TF2 image')
    async def tf2image(self, ctx):
        await ctx.send(random.choice(self.tf2images))

    @commands.command(help='no u')
    async def nou(self, ctx):
        await ctx.send('https://cdn.discordapp.com/attachments/684474004563689539/685130037585772552/deepfried_1583418116265.png')

    # idk about this one -bagguette
    @commands.command(help='gay')
    async def gay(self, ctx):
        await ctx.send('https://www.villagevoice.com/wp-content/uploads/2011/02/thatsgay.png')

    @commands.command(help='Kool aid man doing the sexing ( ͡° ͜ʖ ͡°)')
    async def ohyeah(self, ctx):
        await ctx.send('https://i.pinimg.com/736x/e2/d2/4a/e2d24a8338a81191c59b928c2cbeedcf.jpg')

    @commands.command(help='It rlly is deep tho')
    async def deep(self, ctx):
        await ctx.send('https://preview.redd.it/she0nt0g5b131.jpg?auto=webp&s=e77d77c2bf39d54d9cb89457eee61220d5700df4')

    @commands.command(help='demoman laughing')
    async def laugh(self, ctx):
        await ctx.send('https://i.redd.it/l32xlpu8vad31.jpg')

    @commands.command(help='bruh sound effect #2')
    async def bruh(self, ctx):
        await ctx.send('https://www.youtube.com/watch?v=2ZIpFytCSVc')

    @commands.command(help='You just got vectored')
    async def vector(self, ctx):
        await ctx.send('https://cdn.discordapp.com/attachments/685262422252191781/685591126442377266/download.jpg')

    @commands.command(help='Shows the gonk image')
    async def gonk(self, ctx):
        await ctx.send('https://cdn.discordapp.com/attachments/685262422252191781/685621651970326545/unknown.png')

    @commands.command(help='Shows a random smug anime girl')
    async def smug(self, ctx):
        await ctx.send(random.choice(self.smuganime))

    @commands.command(help='demoman tf2')
    async def didntseethat(self, ctx):
        await ctx.send('https://cdn.discordapp.com/attachments/685262422252191781/689161554318721042/maxresdefault.jpg')

    @commands.command(help='Spycrabs but in vagina')
    async def spycrab(self, ctx):
        await ctx.send('https://i.imgur.com/ufzaw81.png')

    @commands.command(help='Why are you gay')
    async def whygay(self, ctx):
        await ctx.send('https://cdn.discordapp.com/attachments/697102775959552052/704357844572438598/images.jpg')

    @commands.command(help='POV monke')
    async def monke(self, ctx):
        await ctx.send('https://i.redd.it/97vk2gz7zvl41.jpg')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """Adds a reaction to a new reaction within 1 to 3 seconds"""
        if reaction.count != 1: return
        message = reaction.message
        emoji = reaction.emoji
        await asyncio.sleep(random.randint(1, 3))
        await message.add_reaction(emoji)

    @commands.command()
    async def money(self, ctx):
        await ctx.send('https://cdn.discordapp.com/attachments/696786725053399092/717430238941937764/1480273770_spy1.gif')

    @commands.command()
    async def dumbfuck(self, ctx):
        await ctx.send('https://cdn.discordapp.com/attachments/696786725053399092/725474264941330482/vIPF3oY.mp4')

def setup(bot):
    bot.add_cog(SimpleCommands(bot))