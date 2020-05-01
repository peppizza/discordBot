import os
import random
import discord
import aiohttp
import datetime
import asyncio
import secrets

from discord.ext import tasks, commands
from discord import File
from dotenv import load_dotenv
from PIL import Image, ImageFont, ImageDraw

tf2images = ['https://i.ytimg.com/vi/OMUurmalxdc/hqdefault.jpg',
'https://i.redd.it/kyczj16ebgl01.jpg',
'https://i.pinimg.com/736x/a9/c8/ba/a9c8ba036f9ac0bf9637160eb60966b9.jpg',
'https://i.pinimg.com/originals/1a/f8/ef/1af8ef22db24aa35eca301d2d6126992.png',
'https://steamuserimages-a.akamaihd.net/ugc/3245156510465429402/C24E96EE652EF3948771A428C2F082430734E5EB/?imw=1024&imh=640&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=true',
'https://files.gamebanana.com/img/ss/srends/220-90_54f1ddc90108d.jpg',
'https://i.ytimg.com/vi/AtnjFLl6Fnc/maxresdefault.jpg',
'https://wiki.teamfortress.com/w/images/thumb/7/7f/Zombified_Engineer_RED.png/250px-Zombified_Engineer_RED.png',
'https://scontent-atl3-1.cdninstagram.com/v/t51.2885-15/e35/53001684_454915401714262_5744163766126447936_n.jpg?_nc_ht=scontent-atl3-1.cdninstagram.com&_nc_cat=110&_nc_ohc=ByAB04rp3pMAX8f0goS&oh=087304d0e840977dca7dd58ddc8fa891&oe=5EE518A0',
'https://pbs.twimg.com/media/D_ggShHUYAA5jda.png',
'https://i.ytimg.com/vi/1a23gJ40Auo/hqdefault.jpg',
'https://media.discordapp.net/attachments/684474004563689539/684852013313687640/images.jpg',
'https://cdn.discordapp.com/attachments/684474004563689539/685243913925427241/guh.jpg',
'https://cdn.discordapp.com/attachments/684474004563689539/685259476470988995/scout.png',
'https://cdn.discordapp.com/attachments/684474004563689539/685260611655041135/download.jpg',
'https://cdn.discordapp.com/attachments/684474004563689539/685260665782403170/70783045_522992848459733_1340534253499123815_n.jpg',
'https://cdn.discordapp.com/attachments/684474004563689539/685260666612875329/d1m5icxyd3k31.png',
'https://cdn.discordapp.com/attachments/685262422252191781/685282281908207626/s1vnHrPTsVk.jpg',
'https://cdn.discordapp.com/attachments/685262422252191781/685282287759392928/if-u-were-huntin-trouble-lad-ya-found-it-1808-62507520.png',
'https://cdn.discordapp.com/attachments/685262422252191781/685282290707857441/images.jpg',
'https://cdn.discordapp.com/attachments/685262422252191781/685282391681400875/FearfulNauticalBittern-size_restricted.gif',
'https://media.discordapp.net/attachments/685262422252191781/685301796440113160/EGlhe0iWwAAfdjV.png']

smuganime = ['https://i.imgur.com/zZ86SqQ.jpg',
'https://i.imgur.com/kTEdthR.png',
'https://i.imgur.com/ta2hPIP.png',
'https://i.imgur.com/5HLkMUn.jpg',
'https://i.imgur.com/X7d0I0j.jpg',
'https://i.imgur.com/ca7aK06.jpg',
'https://i.imgur.com/J3E5vTj.png',
'https://i.imgur.com/7PtAX3r.jpg',
'https://i.imgur.com/nJeGwtL.png',
'https://i.imgur.com/T9yAcpj.jpg',
'https://i.imgur.com/HQmyxau.jpg',
'https://i.imgur.com/zxAZa8v.png',
'https://i.imgur.com/nBd6FOZ.jpg',
'https://i.imgur.com/c1sEDv6.jpg',
'https://i.imgur.com/jSfSm9i.jpg',
'https://i.imgur.com/9ozFx6l.jpg',
'https://i.imgur.com/Pm9iWoC.png',
'https://i.imgur.com/W3hDdoN.jpg',
'https://i.imgur.com/2zsRjT4.jpg',
'https://i.imgur.com/NcdUm1z.jpg',
'https://i.imgur.com/I4KC8iY.jpg',
'https://i.imgur.com/nwIZ18D.jpg',
'https://i.imgur.com/N1j4MtI.jpg',
'https://i.imgur.com/SDZiYbO.jpg',
'https://i.imgur.com/lxzx05z.png',
'https://i.imgur.com/yTIQi08.jpg',
'https://i.imgur.com/wtJoU5i.jpg',
'https://i.imgur.com/rBNdIyv.png',
'https://i.imgur.com/KvqK5v2.jpg',
'https://i.imgur.com/jyBx8ey.jpg',
'https://i.imgur.com/n9scBQJ.png',
'https://i.imgur.com/Ymh3bu8.jpg',
'https://i.imgur.com/P2okGZL.png',
'https://i.imgur.com/UB589Gj.jpg',
'https://i.imgur.com/LAr0sNk.png',
'https://i.imgur.com/YziqTr8.jpg',
'https://i.imgur.com/qxNrURN.jpg',
'https://i.imgur.com/0ykfocu.jpg',
'https://i.imgur.com/YSMTW4M.jpg',
'https://i.imgur.com/t0xcafa.jpg',
'https://i.imgur.com/rLmY9Ih.jpg',
'https://i.imgur.com/GijKuII.jpg',
'https://i.imgur.com/Q2qVSHi.jpg',
'https://i.imgur.com/p3bBAbv.png',
'https://i.imgur.com/Vm5Rp3F.png',
'https://i.imgur.com/Z2YazV2.png',
'https://i.imgur.com/MY3Y2oe.png',
'https://i.imgur.com/nYGqtmm.jpg',
'https://i.imgur.com/SIASCpk.png',
'https://i.imgur.com/FKmk4W2.jpg',
'https://i.imgur.com/wmDFzgn.png',
'https://i.imgur.com/9dch3WI.jpg',
'https://i.imgur.com/8kEvBrW.jpg',
'https://i.imgur.com/PtfUGcW.jpg',
'https://i.imgur.com/nUKajp8.jpg',
'https://i.imgur.com/wpm5nbC.jpg',
'https://i.imgur.com/5xVHRoZ.jpg',
'https://i.imgur.com/2b1EgRt.gif',
'https://i.imgur.com/ZjEJPSF.jpg',
'https://i.imgur.com/FMX3JWc.jpg',
'https://i.imgur.com/VJrCLRZ.gif',
'https://i.imgur.com/PgXczVM.jpg',
'https://i.imgur.com/ifn0y3R.jpg',
'https://i.imgur.com/vsjIHCB.gif',
'https://i.imgur.com/4KGJcgn.jpg',
'https://i.imgur.com/GG5yVYI.gif',
'https://i.imgur.com/klnQX0G.jpg',
'https://i.imgur.com/YEENPxn.jpg',
'https://i.imgur.com/zcW6SGe.jpg',
'https://i.imgur.com/g6Z2qTv.png',
'https://i.imgur.com/i3z089c.gif',
'https://i.imgur.com/nNscc33.jpg',
'https://i.imgur.com/II9C64i.jpg',
'https://i.imgur.com/Gwws0sb.jpg',
'https://i.imgur.com/Qbn9oiE.jpg',
'https://i.imgur.com/qH8XU5u.jpg',
'https://i.imgur.com/QA6miqk.jpg',
'https://i.imgur.com/YBgt6Fp.png',
'https://i.imgur.com/keIjvp6.png',
'https://i.imgur.com/Lcy2ka1.jpg',
'https://i.imgur.com/8lIFT9V.jpg',
'https://i.imgur.com/0Eu67Iy.png',
'https://i.imgur.com/Bt7P0jO.png',
'https://i.imgur.com/zhSqk20.jpg',
'https://i.imgur.com/PBsIILk.jpg',
'https://i.imgur.com/tgcnQKt.jpg',
'https://i.imgur.com/khe64CV.png',
'https://i.imgur.com/n1bBsCE.jpg',
'https://i.imgur.com/fNtvUyA.jpg',
'https://i.imgur.com/UOdbHbW.png',
'https://i.imgur.com/ZMF4VB9.jpg',
'https://i.imgur.com/oqnqW94.jpg',
'https://i.imgur.com/PKQv0hv.png',
'https://i.imgur.com/Szxalw8.png',
'https://i.imgur.com/guJ03ZP.png',
'https://i.imgur.com/ilVwbzh.jpg',
'https://i.imgur.com/i3vPyi4.jpg',
'https://i.imgur.com/oE0zh5l.png',
'https://i.imgur.com/YPjzyLJ.jpg',
'https://i.imgur.com/NJwrb6v.png',
'https://i.imgur.com/f46gfL7.png',
'https://i.imgur.com/XH8XcPB.jpg',
'https://i.imgur.com/RcbZQ5R.jpg',
'https://i.imgur.com/WHzDhN8.jpg',
'https://i.imgur.com/HAiBatu.jpg',
'https://i.imgur.com/dr1k07L.jpg',
'https://i.imgur.com/DxTS9cq.jpg',
'https://i.imgur.com/iQesLYW.jpg',
'https://i.imgur.com/NiB87nf.jpg',
'https://i.imgur.com/WqnldbG.jpg',
'https://i.imgur.com/9ewIvkO.jpg',
'https://i.imgur.com/rksgpaB.jpg',
'https://i.imgur.com/sbIbKe5.jpg',
'https://i.imgur.com/yGHqFyb.jpg',
'https://i.imgur.com/RXhecde.png',
'https://i.imgur.com/aQspnK5.png',
'https://i.imgur.com/u2kLxQG.jpg',
'https://i.imgur.com/HhkIWhw.gif',
'https://i.imgur.com/gJCeCx0.jpg',
'https://i.imgur.com/2cjOFN8.jpg',
'https://i.imgur.com/2Cs1ClO.jpg',
'https://i.imgur.com/DuFMOaa.jpg',
'https://i.imgur.com/Qv7lvI4.jpg',
'https://i.imgur.com/I845vm9.jpg',
'https://i.imgur.com/jWGa1Wv.jpg',
'https://i.imgur.com/JQxUJfh.jpg',
'https://i.imgur.com/01DmNfA.jpg',
'https://i.imgur.com/Hw3XXjd.jpg',
'https://i.imgur.com/ltTk3g4.jpg',
'https://i.imgur.com/a9L2SJ9.jpg',
'https://i.imgur.com/rW1IKH0.jpg',
'https://i.imgur.com/sAV3Dhe.jpg',
'https://i.imgur.com/xuVRgf0.png',
'https://i.imgur.com/SW9Yo6W.png',
'https://i.imgur.com/CmeGLy0.png',
'https://i.imgur.com/rYJ4KSA.jpg',
'https://i.imgur.com/NTQhdze.png',
'https://i.imgur.com/lYdaCiv.jpg',
'https://i.imgur.com/Ux56xzx.jpg',
'https://i.imgur.com/9ccemGP.png',
'https://i.imgur.com/Qs4T8qw.jpg',
'https://i.imgur.com/yWw3Z4d.jpg',
'https://i.imgur.com/L6drc5y.jpg',
'https://i.imgur.com/DKvuC4x.png',
'https://i.imgur.com/daSUBUq.jpg',
'https://i.imgur.com/WMarmXH.jpg',
'https://i.imgur.com/Suwg5Y1.jpg',
'https://i.imgur.com/FFYxzF0.jpg',
'https://i.imgur.com/EYGvoQP.jpg',
'https://i.imgur.com/EqPYUBC.jpg',
'https://i.imgur.com/i34rCCQ.jpg',
'https://i.imgur.com/Zmp2tK1.jpg',
'https://i.imgur.com/vXduNtM.jpg',
'https://i.imgur.com/iJHkZ0u.jpg',
'https://i.imgur.com/egAeddZ.png',
'https://i.imgur.com/02RIEW1.jpg',
'https://i.imgur.com/qR5OuFk.jpg',
'https://i.imgur.com/04M0UD2.jpg',
'https://i.imgur.com/hdLhHB1.jpg',
'https://i.imgur.com/dVXL8lu.gif',
'https://i.imgur.com/Xi4dDOz.jpg',
'https://i.imgur.com/I6Lhgel.jpg',
'https://i.imgur.com/sBjMGxd.jpg',
'https://i.imgur.com/PYPpjBv.jpg',
'https://i.imgur.com/6jHUoLB.jpg',
'https://i.imgur.com/rVE7H6R.jpg',
'https://i.imgur.com/g6Fiv1G.png',
'https://i.imgur.com/tyw2H0Y.jpg',
'https://i.imgur.com/uFn0Uxf.png',
'https://i.imgur.com/K1KCYfz.jpg',
'https://i.imgur.com/SC6URzX.png',
'https://i.imgur.com/xdMO1pY.jpg',
'https://i.imgur.com/BcbnCjI.png',
'https://i.imgur.com/t5Fx13D.jpg',
'https://i.imgur.com/hlxdHQD.jpg',
'https://i.imgur.com/ODhB2nV.png',
'https://i.imgur.com/iTvpfKj.jpg',
'https://i.imgur.com/WUNircv.jpg',
'https://i.imgur.com/Pp4a8li.png',
'https://i.imgur.com/9UQnMPu.png',
'https://i.imgur.com/qPlEQbP.gif',
'https://i.imgur.com/9d8h1Zi.jpg',
'https://i.imgur.com/bNWZeOL.png',
'https://i.imgur.com/U9GIevx.jpg',
'https://i.imgur.com/bsJ8Y9o.jpg',
'https://i.imgur.com/3x5urU9.jpg',
'https://i.imgur.com/U6CRbTm.gif',
'https://i.imgur.com/m0XObx2.jpg',
'https://i.imgur.com/rnRf07K.jpg',
'https://i.imgur.com/vwMPSzM.gif',
'https://i.imgur.com/sV9eaDi.jpg',
'https://i.imgur.com/CvN5HUx.jpg',
'https://i.imgur.com/CrFEyPz.jpg',
'https://i.imgur.com/0WnizAm.jpg',
'https://i.imgur.com/n3nRGXa.jpg',
'https://i.imgur.com/tdlOLZD.jpg',
'https://i.imgur.com/QwdMPCo.jpg',
'https://i.imgur.com/CEzHAZd.jpg',
'https://i.imgur.com/d8gx4Nl.png',
'https://i.imgur.com/fruMBav.jpg',
'https://i.imgur.com/ZLSyvBX.png',
'https://i.imgur.com/hica49P.png',
'https://i.imgur.com/NZ7E5GA.jpg',
'https://i.imgur.com/gb9oA7j.jpg',
'https://i.imgur.com/hMvZing.jpg',
'https://i.imgur.com/U6V5yYh.jpg',
'https://i.imgur.com/t2VCO3z.jpg',
'https://i.imgur.com/DOLl4Ew.png',
'https://i.imgur.com/SO5zzgy.jpg',
'https://i.imgur.com/Gmtl0B4.jpg',
'https://i.imgur.com/KkIwFHI.png',
'https://i.imgur.com/ruSijCe.jpg',
'https://i.imgur.com/h9J2EkX.gif',
'https://i.imgur.com/TNURnpS.jpg',
'https://i.imgur.com/tyTrxt6.jpg',
'https://i.imgur.com/uwu0BIq.jpg',
'https://i.imgur.com/g1xbLhn.jpg',
'https://i.imgur.com/NPV43uL.jpg',
'https://i.imgur.com/Ak6VeeP.png',
'https://i.imgur.com/HnirTG3.png',
'https://i.imgur.com/IA6OerY.jpg',
'https://i.imgur.com/6iwfHVG.png',
'https://i.imgur.com/ebQOEYu.png',
'https://i.imgur.com/Hc1Kdg3.png',
'https://i.imgur.com/wUkkzMM.png',
'https://i.imgur.com/TVE6VaQ.png',
'https://i.imgur.com/XP37eJ5.png',
'https://i.imgur.com/3j7akLB.gif',
'https://i.imgur.com/ybWkSdy.gif',
'https://i.imgur.com/nnORbAh.gif',
'https://i.imgur.com/nZQekmY.jpg',
'https://i.imgur.com/ZkNZ6aF.jpg',
'https://i.imgur.com/wlQBcqH.png',
'https://i.imgur.com/UpX3hIb.png',
'https://i.imgur.com/gJtBQz0.gif',
'https://i.imgur.com/RNiA6SO.jpg',
'https://i.imgur.com/yJOOaHY.gif',
'https://i.imgur.com/ci1pwlq.png',
'https://i.imgur.com/UHexbYa.png',
'https://i.imgur.com/uBrAFs9.jpg',
'https://i.imgur.com/ajGTQoF.jpg',
'https://i.imgur.com/JXZ2Z5w.png',
'https://i.imgur.com/gf4eUIk.jpg',
'https://i.imgur.com/iKiugeP.png',
'https://i.imgur.com/GVVJOsy.png',
'https://i.imgur.com/ql4AD6G.png',
'https://i.imgur.com/YtQTtV7.png',
'https://i.imgur.com/xNI58Yh.png',
'https://i.imgur.com/sprYWgu.png',
'https://i.imgur.com/Ciih6uK.gif',
'https://i.imgur.com/euyOgLk.jpg',
'https://i.imgur.com/thsfR33.gif',
'https://i.imgur.com/xuZNYDq.png',
'https://i.imgur.com/AZ9UidF.png',
'https://i.imgur.com/rEWwjXF.jpg',
'https://i.imgur.com/pxrzoKF.gif',
'https://i.imgur.com/H9oKZXz.png']

suggestions = [697102775959552052, 702882611256754289, 702882635365613662, 703312812096749599, 703312842715037766, 703312883055984730, 703312953637863515, 703313003889688696, 703313116154560583]
bannedwords = ['nigger', 'nigga', 'faggot', 'fag', 'dyke', 'niggers', 'niggas', 'faggots', 'fags']

# https://dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={key}


load_dotenv()
token = os.getenv('DISCORD_TOKEN')
key = os.getenv('API_KEY')
bday = datetime.datetime(2020, 10, 26)

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='dm me !report to report a user'))

class SuggestionHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.inactivesuggestions = []
        self.bannedusers = []

    async def inactivetoopen(self):
        opencategory = bot.get_channel(702882329332285471)
        if len(opencategory.channels) < 2:
            inactivecategory = bot.get_channel(703314675529416785)
            for channels in inactivecategory.channels:
                print(channels.id)
                self.inactivesuggestions.append(channels.id)
        chosen = random.choice(self.inactivesuggestions)
        chosen = bot.get_channel(chosen)
        category = bot.get_channel(702882329332285471)
        await chosen.edit(name='{}-✅'.format(chosen.name).replace('⌛', ''), category=category, sync_permissions=True)
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
            NotImplementedError
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
        else:
            NotImplementedError

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
        times = int(arg2)
        if (times <= 10):
            for i in range(times):
                await ctx.send(arg1)
        else:
            await ctx.send(ctx, OverflowError)

    @ping.error
    async def ping_on_error(self, ctx, error):
        await ctx.send('ping limit is 10')

    @commands.command()
    async def dio(self, ctx, *args):
        W = 1280
        msg = " ".join(args[:]).upper()
        if len(msg) <= 18:
            fontSize = 144
        elif len(msg) <= 25:
            fontSize = 100
        elif len(msg) <= 30:
            fontSize = 70
        else:
            fontSize = 50

        font = ImageFont.truetype("/usr/share/fonts/truetype/msttcorefonts/Impact.ttf", fontSize)
        img = Image.open('dio.jpg')
        draw = ImageDraw.Draw(img)
        w = draw.textsize(msg, font=font)[0]
        async with ctx.typing():
            draw.text(((W-w)/2, 0), msg, (255, 255, 255), font=font)
            img.save("final.png")
            await ctx.send(file=File('final.png'))

    @dio.error
    async def dio_on_error(self, ctx, error):
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
        await ctx.send('set a reminder \"{0}\" for <@!{1}> for {2}'.format(' '.join(args[1:]), author, args[0]))
        await asyncio.sleep(convert(args[0]))
        await ctx.send('<@!{0}> {1}'.format(author, ' '.join(args[1:])))

    @remindme.error
    async def remindme_on_error(self, ctx, error):
        await ctx.send(error)

class SimpleCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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

    @commands.command(name='siegheil', help='hitler')
    async def hitler(self, ctx):
        await ctx.send('https://www.youtube.com/watch?v=lLwguZnvguQ')

    @commands.command(help='shrek')
    async def shrek(self, ctx):
        await ctx.send('https://www.youtube.com/watch?v=psFzJv8g6jc')

    @commands.command(name='hamburger10hours', help='hamburger')
    async def hamburger(self, ctx):
        await ctx.send('https://www.youtube.com/watch?v=qIJ-lchwqVA')

    @commands.command(name='tf2image', help='selects random tf2 image')
    async def tf2(self, ctx):
        await ctx.send(secrets.choice(tf2images))

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
        await ctx.send(secrets.choice(smuganime))

    @commands.command(help='demoman tf2')
    async def didntseethat(self, ctx):
        await ctx.send('https://cdn.discordapp.com/attachments/685262422252191781/689161554318721042/maxresdefault.jpg')

    @commands.command()
    async def spycrab(self, ctx):
        await ctx.send('https://i.imgur.com/ufzaw81.png')

    @commands.command()
    async def whygay(self, ctx):
        await ctx.send('https://cdn.discordapp.com/attachments/697102775959552052/704357844572438598/images.jpg')

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
    async def on_message(self, message):
        for word in message.content.split():
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
        await member.send(embed=embed)
        if auto == False:
            embed2 = discord.Embed(title='{} has been warned'.format(member), description='**{}** has been warned by **{}** for **{}**'.format(member, ctx.author, ' '.join(args[0:])))
        else:
            embed2 = discord.Embed(title='{} has been warned'.format(member), description='**{}** has been automatically warned for hate speech'.format(member))
        await channel.send(embed=embed2)

    @warn.error
    async def warn_on_error(self, ctx, error):
        await ctx.message.delete()
        print(error)
    

if __name__ == '__main__':
    bot.add_cog(SuggestionHandler(bot))
    bot.add_cog(ArgCommands(bot))
    bot.add_cog(SimpleCommands(bot))
    bot.add_cog(DmCommands(bot))
    bot.add_cog(VoiceCommands(bot))
    bot.add_cog(Moderation(bot))
    bot.run(token)
