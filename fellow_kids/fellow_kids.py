import os
import discord
import aiohttp
import asyncio
import secrets
import json
import logging

from discord.ext import commands
from discord import File
from dotenv import load_dotenv
from PIL import Image, ImageFont, ImageDraw

suggestions = [697102775959552052, 702882611256754289, 702882635365613662, 703312812096749599, 703312842715037766, 703312883055984730, 703312953637863515, 703313003889688696, 703313116154560583]
bannedwords = ['nigger', 'nigga', 'faggot', 'fag', 'dyke', 'niggers', 'niggas', 'faggots', 'fags']

# https://dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={key}


load_dotenv()
token = os.getenv('DISCORD_TOKEN')
key = os.getenv('API_KEY')

logging.basicConfig(level=logging.INFO)
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='dm me !report to report a user'))

class SuggestionHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bannedusers = []

    async def inactivetoopen(self):
        inactivesuggestions = []
        opencategory = bot.get_channel(702882329332285471)
        if len(opencategory.channels) < 2:
            inactivecategory = bot.get_channel(703314675529416785)
            for channels in inactivecategory.channels:
                inactivesuggestions.append(channels.id)
        chosen = secrets.choice(inactivesuggestions)
        chosen = bot.get_channel(chosen)
        await chosen.edit(name='{}-✅'.format(chosen.name).replace('⌛', ''), category=opencategory, sync_permissions=True)
        embed = discord.Embed(title='open', description='this channel is now open for suggestions', color=0x00ff00)
        await chosen.send(embed=embed)


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in suggestions:
            channel = message.channel
            catagory = channel.category
            if catagory.id == 702882329332285471 and message.author.id != 681886537046163506 and message.author.id != 253290704384557057 and message.author.id != 704350265590939649 and not message.author.id in self.bannedusers:
                embed = discord.Embed(title='working on..', description='Your request is now being worked on by the devs', color=0x00ff00)
                category = bot.get_channel(702882449159618663)
                guild = message.guild
                everyone = guild.get_role(684472795639447621)
                dev = guild.get_role(697125812465565746)
                await channel.edit(name='{}-⌛'.format((message.channel.name).replace('✅', '')), category=category)
                await channel.set_permissions(message.author, send_messages=True)
                await channel.set_permissions(everyone, send_messages=False)
                await channel.set_permissions(dev, send_messages=True)
                await channel.send('<@!{}>'.format(253290704384557057), embed=embed)
                await self.inactivetoopen()

    @commands.command(aliases=['done'])
    async def close(self, ctx):
        channel = ctx.message.channel
        category = bot.get_channel(703314675529416785)
        embed = discord.Embed(title='inactive', description='this channel is now inactive', color=0x000000)
        await channel.edit(name=str(channel.name).replace('⌛', ''), category=category, sync_permissions=True)
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.has_role(696773209495699547)
    async def nosuggest(self, ctx, member: discord.Member):
        self.bannedusers.append(member.id)
    
    @commands.command()
    @commands.has_role(696773209495699547)
    async def suggest(self, ctx, member: discord.Member):
        self.bannedusers.remove(member.id)

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
        await ctx.send('you fucked up the command you peice of subhuman trash')


    @commands.command(help='beanify')
    @commands.has_role('Moderators')
    async def bean(self, ctx, *args):
        if (args == ()):
            await ctx.send('Please provide an argument for beaning')
        elif (len(args) == 1):
            embed = discord.Embed(title="bean", description="you have been beaned", color=0xff0000)
            embed.set_author(name=ctx.message.author.name)
            embed.add_field(name="person", value=args[0])
            embed.set_image(url="https://images.immediate.co.uk/production/volatile/sites/4/2018/08/GettyImages-149069817-15d7368.jpg?webp=true&quality=45&resize=1880%2C799")
            await ctx.send(embed=embed)
        elif (len(args) >= 2):
            embed = discord.Embed(title="bean", description="you have been beaned", color=0xff0000)
            embed.set_author(name=ctx.message.author.name)
            embed.add_field(name="person", value=args[0])
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
        if int(arg2) > 10:
            await ctx.send("ping limit is ten")
            return
        final = int(arg2) * (arg1 + '\n')
        await ctx.send(final)

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
                    async with session.get('https://dictionaryapi.com/api/v3/references/thesaurus/json/{}?key={}'.format(word, key)) as r:
                        if r.status == 200:
                            js = await r.json()
                            try:
                                word = js[0]['meta']['syns'][0]
                                word = secrets.choice(word)
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

class SimpleCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open('assets/images.json', 'r') as in_file:
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

    @commands.command(name='youneedjesus', help='jesus')
    async def jesus(self, ctx):
        await ctx.send('https://www.you-need-jesus.com/')

    @commands.command(name='momsahoe', help='your mom be a hoe')
    async def mom(self, ctx):
        await ctx.send('https://www.youtube.com/watch?v=iYx_aGlmyc4')

    @commands.command(help='heyayayaya')
    async def hey(self, ctx):
        await ctx.send('https://www.youtube.com/watch?v=ZZ5LpwO-An4&t=13s')

    @commands.command(help='shrek')
    async def shrek(self, ctx):
        await ctx.send('https://www.youtube.com/watch?v=psFzJv8g6jc')

    @commands.command(name='hamburger10hours', help='hamburger')
    async def hamburger(self, ctx):
        await ctx.send('https://www.youtube.com/watch?v=qIJ-lchwqVA')

    @commands.command(name='tf2image', help='selects random tf2 image')
    async def tf2(self, ctx):
        await ctx.send(secrets.choice(self.tf2images))

    @commands.command(help='no u')
    async def nou(self, ctx):
        await ctx.send('https://cdn.discordapp.com/attachments/684474004563689539/685130037585772552/deepfried_1583418116265.png')

    @commands.command(help='gay')
    async def gay(self, ctx):
        await ctx.send('https://www.villagevoice.com/wp-content/uploads/2011/02/thatsgay.png')

    @commands.command(name='ohyeah', help='kool aid man')
    async def yeah(self, ctx):
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
        await ctx.send('https://cdn.discordapp.com/attachments/685262422252191781/685621651970326545/unknown.png')

    @commands.command(help='prints smug anime girl')
    async def smug(self, ctx):
        await ctx.send(secrets.choice(self.smuganime))

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
        message = reaction.message
        emoji = reaction.emoji
        await message.add_reaction(emoji)

    @commands.command()
    async def money(self, ctx):
        await ctx.send('https://cdn.discordapp.com/attachments/696786725053399092/717430238941937764/1480273770_spy1.gif')

class DmCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.dm_only()
    async def report(self, ctx):
        await ctx.send('https://forms.gle/bwfdc1AyHJ5dL1ZN7')

    @report.error
    async def report_on_error(self, ctx, error):
        await ctx.message.delete()
        await ctx.message.author.send('Please dm me the report command')

class VoiceCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def running(self, ctx):
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('assets/Why are You Running.mp3'))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    @commands.command()
    async def dead(self, ctx):
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('assets/Heavy is Dead.mp3'))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
    
    @commands.command()
    async def yankee(self, ctx):
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('assets/YANKEE WITH NO BRIM.mp3'))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    @commands.command()
    async def jojo(self, ctx):
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('assets/Goodbye Jojo.mp3'))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    @running.before_invoke
    @dead.before_invoke
    @yankee.before_invoke
    @jojo.before_invoke
    async def join(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()
    
class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        new_people = bot.get_channel(704404601327321149)
        rules = bot.get_channel(704737000078704710)
        promotion = bot.get_channel(704775810199846973)
        embed = discord.Embed(title='Welcome {}!'.format(member.name), description='Head to {} for the rules,\n{} for self-promotion,\nand feel free to make a suggestion!'.format(rules.mention, promotion.mention))
        await new_people.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        for word in message.content.split():
            word = word.replace('_', '')
            word = word.replace('*', '')
            word = word.replace('~', '')
            word = word.replace('`', '')
            if word.lower() in bannedwords:
                context = await bot.get_context(message=message)
                await self.warn(context, context.author, ('Hate speech'), auto=True)

    @commands.command()
    @commands.has_role(696773209495699547)
    async def warn(self, ctx, member: discord.Member, *args, auto=False):
        channel = bot.get_channel(685262422252191781)
        await ctx.message.delete()
        embed = discord.Embed(title='WARNING')
        embed.add_field(name='you have been warned by', value=ctx.message.author)
        embed.add_field(name='reason', value=' '.join(args[0:]))
        if not ctx.author.bot:
            await member.send(embed=embed)
        if auto == False:
            embed = discord.Embed(title='{} has been warned'.format(member), description='**{}** has been warned by **{}**'.format(member, ctx.author))
            embed.add_field(name='Reason', value=' '.join(args[0:]))
        else:
            embed = discord.Embed(title='{} has been warned'.format(member), description='**{}** has been automatically warned for hate speech'.format(member))
            embed.add_field(name='original message', value=ctx.message.content)
        await channel.send(embed=embed)

    @warn.error
    async def warn_on_error(self, ctx, error):
        await ctx.message.delete()
        print(error)

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
        with open('level.json', 'r') as read_file:
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

        with open('level.json', 'w') as write_file:
            json.dump(data, write_file)

    @commands.command()
    async def level(self, ctx):

        user = str(ctx.author.id)
        
        with open('level.json', 'r') as read_file:
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
    @commands.has_role(684473159956824143)
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
            open('level.json', 'w').write('{}')
            await ctx.send('Erased levels')
        
    @commands.command()
    @commands.has_role(684473159956824143)
    async def cancel(self, ctx):
        self.erase = False
        await ctx.send('Rocket launch canceled')

    @commands.command()
    @commands.has_role(684473159956824143)
    async def count(self, ctx, member: discord.Member, level: int, custom=''):
        with open('level.json', 'r') as in_file:
            data = json.load(in_file)

        user = str(member.id)
        if user in data:
            data[user][0] = level
            if custom != '':
                data[user][1] = custom

        with open('level.json', 'w') as out_file:
            json.dump(data, out_file)

    @count.error
    async def count_on_error(self, ctx, error):
        await ctx.send(error)

class imageDraw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dio(self, ctx, *args):
        if self.filter(' '.join(args[:])):
            return
        W = 1280
        msg = ' '.join(args[:]).upper()
        if len(msg) <= 18:
            fontSize = 144
        elif len(msg) <= 25:
            fontSize = 100
        elif len(msg) <= 30:
            fontSize = 70
        else:
            fontSize = 50

        font = ImageFont.truetype("/usr/share/fonts/truetype/msttcorefonts/Impact.ttf", fontSize)
        await self.drawText(ctx, msg, font, W, 'dio.jpg')

    # @commands.command()
    # async def line(self, ctx, *args):
    #     if self.filter(' '.join(args[:]))

    async def drawText(self, ctx, text, font, W, image):
        img = Image.open(image)
        draw = ImageDraw.Draw(img)
        w = draw.textsize(text, font=font)[0]
        async with ctx.typing():
            draw.text(((W-w)/2, 0), text, (255, 255, 255), font=font)
            img.save('final.png')
            await ctx.send(file=File('final.png'))

    def filter(self, text):
        text = text.replace('_', '')
        text = text.replace('*', '')
        text = text.replace('~', '')
        text = text.replace('`', '')
        for word in text.split():
            if word.lower() in bannedwords:
                return True

        return False


if __name__ == '__main__':
    bot.add_cog(SuggestionHandler(bot))
    bot.add_cog(ArgCommands(bot))
    bot.add_cog(SimpleCommands(bot))
    bot.add_cog(DmCommands(bot))
    bot.add_cog(VoiceCommands(bot))
    bot.add_cog(Moderation(bot))
    bot.add_cog(Leveling(bot))
    bot.add_cog(imageDraw(bot))
    bot.run(token)
