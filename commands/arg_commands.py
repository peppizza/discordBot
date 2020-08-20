import discord
import aiohttp
import random
import os
import warnings

from discord.ext import commands

class ArgCommands(commands.Cog):

    def __init__(self, bot: commands.AutoShardedBot):
        """Simple commands that contain arguments."""
        self.bot = bot
        if os.environ.get('IS_IN_DOCKER', None):
            self.API_KEY = os.getenv('MERRIAM_TOKEN')
            if self.API_KEY is None:
                warnings.warn('The dictionaryapi token was not found, mimic will not be availible')
                self.is_mimic_availible = False
            else:
                self.is_mimic_availible = True
        else:
            from json import load
            with open('config.json', 'r') as in_file:
                config = load(in_file)
                if 'MERRIAM_TOKEN' in config:
                    self.API_KEY = config['MERRIAM_TOKEN']
                    self.is_mimic_availible = True
                else:
                    warnings.warn('The dictionaryapi token was not found, mimic will not be availible')
                    self.is_mimic_availible = False

    @commands.command(help='kill someone')
    async def die(self, ctx, arg):
        await ctx.send(f'{arg}, kys')

    @die.error
    async def die_on_error(self, ctx, error):
        await ctx.send('you fucked up the command you piece of subhuman trash')


    @commands.command(help='beanify')
    @commands.has_role('Moderators')
    async def bean(self, ctx, *args):
        if not args:
            await ctx.send('Please provide an argument for beaning')
            return
        embed = discord.Embed(title="bean", description="you have been beaned", color=0xff0000)
        embed.set_author(name=ctx.message.author.name)
        embed.add_field(name="person", value=args[0])
        if len(args) >= 2:
            embed.add_field(name="reason", value=' '.join(args[1: len(args)]))
        embed.set_image(url="https://images.immediate.co.uk/production/volatile/sites/4/2018/08/GettyImages-149069817-15d7368.jpg?webp=true&quality=45&resize=1880%2C799")
        await ctx.send(embed=embed)

    @bean.error
    async def bean_on_error(self, ctx, error):
        await ctx.send(error)

    @commands.command(help='bonk')
    async def bonk(self, ctx, arg):
        await ctx.send('{} has been bonked'.format(arg))

    @bonk.error
    async def bonk_on_error(self, ctx, error):
        await ctx.send(error)

    @commands.command(help='ping')
    @commands.has_role('pinging rights')
    async def ping(self, ctx, arg1, arg2):
        try:
            i = int(arg2)
        except ValueError:
            await ctx.send('{} is not a number'.format(arg2))
            return
        if i > 10 or i <= 0:
            await ctx.send("Number must be between 1 and 10")
            return
        await ctx.send(i * (arg1 + '\n'))

    @ping.error
    async def ping_on_error(self, ctx, error):
        await ctx.send(error)

    @commands.command()
    @commands.has_role('Moderators')
    async def mute(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name='Muted')
        await member.add_roles(role)
        await ctx.send('this american boot just muted your american ass back to american canada\nBECAUSE AMERICA')

    @mute.error
    async def mute_on_error(self, ctx, error):
        await ctx.send(error)

    @commands.command()
    @commands.has_role('Moderators')
    async def unmute(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name='Muted')
        await member.remove_roles(role)

    @commands.command()
    async def mimic(self, ctx, member: discord.Member):

        if member.bot: return

        def check(m):
            return m.author == member

        msg = await self.bot.wait_for('message', check=check)
        final = str(msg.content)

        wordlist = []
        async with ctx.typing():
            for word in final.split():
                async with aiohttp.ClientSession() as session:
                    async with session.get('https://dictionaryapi.com/api/v3/references/thesaurus/json/{}?key={}'.format(word, self.API_KEY)) as r:
                        if r.status == 200:
                            js = await r.json()
                            try:
                                word = js[0]['meta']['syns'][0]
                                word = random.choice(word)
                                wordlist.append(word)
                            except Exception:
                                wordlist.append(word)

        await ctx.send(' '.join(wordlist))

    @commands.command(aliases=['emoji'])
    async def emote(self, ctx, emoji: discord.Emoji):
        await ctx.send(emoji.url)

def setup(bot):
    bot.add_cog(ArgCommands(bot))