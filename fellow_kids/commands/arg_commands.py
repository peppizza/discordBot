import discord
import asyncio
import aiohttp
import random

from fellow_kids.fellow_kids import API_KEY

class ArgCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(help='kill someone')
    async def die(self, ctx, arg):
        if arg == '<@!681886537046163506>':
            await bot.change_presence(status=discord.Status.invisible)
            await asyncio.sleep(5)
            await ctx.send('Like jesus I too have respawned')
            await bot.change_presence(status=discord.Status.online)
        else:
            await ctx.send(f'{arg}, kys')

    @die.error
    async def die_on_error(self, ctx, error):
        await ctx.send('you fucked up the command you piece of subhuman trash')


    @commands.command(help='beanify')
    @commands.has_role('Moderators')
    async def bean(self, ctx, *args):
        if (args == ()):
            await ctx.send('Please provide an argument for beaning')
            return
        embed = discord.Embed(title="bean", description="you have been beaned", color=0xff0000)
        embed.set_author(name=ctx.message.author.name)
        embed.add_field(name="person", value=args[0])
        if(len(args) >= 2):
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

        msg = ()

        def check(m):
            return m.author == member

        msg = await bot.wait_for('message', check=check)
        final = str(msg.content)

        wordlist = []
        async with ctx.typing():
            for word in final.split():
                async with aiohttp.ClientSession() as session:
                    async with session.get('https://dictionaryapi.com/api/v3/references/thesaurus/json/{}?key={}'.format(word, API_KEY)) as r:
                        if r.status == 200:
                            js = await r.json()
                            try:
                                word = js[0]['meta']['syns'][0]
                                word = random.choice(word)
                                wordlist.append(word)
                            except Exception:
                                wordlist.append(word)

        await ctx.send(' '.join(wordlist))

    @commands.command()
    async def remindme(self, ctx, *args):
        author = ctx.message.author.id
        def convert(time):
            indicators = ['hr', 'min', 'sec']
            if any(substring in time for substring in indicators):
                originaltime = time
                time = time.replace('hr', '')
                time = time.replace('min', '')
                time = time.replace('sec', '')
                time = int(time)
                if 'hr' in originaltime:
                    time = time * 3600
                elif 'min' in originaltime:
                    time = time * 60
                return time
        await ctx.send('set a reminder \"{}\" for {} for {}'.format(' '.join(args[1:]), author.mention, args[0]))
        await asyncio.sleep(convert(args[0]))
        await ctx.send('{} {}'.format(author.mention, ' '.join(args[1:])))

    @remindme.error
    async def remindme_on_error(self, ctx, error):
        await ctx.send(error)

    @commands.command(aliases=['emoji'])
    async def emote(self, ctx, emoji: discord.Emoji):
        await ctx.send(emoji.url)
