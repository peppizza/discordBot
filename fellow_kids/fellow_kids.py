import os
import random
import discord
import requests
import json
import datetime
import asyncio

from discord.ext import commands
from discord import File
from dotenv import load_dotenv
from PIL import Image, ImageFont, ImageDraw
from time import sleep

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

# https://dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={key}


load_dotenv()
token = os.getenv('DISCORD_TOKEN')
key = os.getenv('API_KEY')
bday = datetime.datetime(2020, 10, 26)

bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'))

def getapi(word):
    response = requests.get('https://dictionaryapi.com/api/v3/references/thesaurus/json/{0}?key={1}'.format(word, key))
    parsed = response.json()
    try:
        syns = parsed[0]['meta']['syns'][0]
        return random.choice(syns)
    except TypeError or IndexError:
        return word
    

@bot.event
async def on_message(message):
    if message.content.startswith('okay'):
        channel = message.channel
        await channel.send('ok>okay')
    await bot.process_commands(message)

@bot.command(help='kill someone')
async def die(ctx, arg):
    if arg == '<@!681886537046163506>':
        await bot.change_presence(status=discord.Status.invisible)
        sleep(5)
        await ctx.send('Like jesus I too have respawned')
        await bot.change_presence(status=discord.Status.online)
    else:
        await ctx.send(f'{arg}, kys')

@die.error
async def die_on_error(ctx, error):
    await ctx.send('you fucked up the command you peice of subhuman trash')

@bot.command(help='rick roll')
async def rr(ctx):
    await ctx.send('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

@bot.command(help='say the n word')
async def nword(ctx):
    await ctx.send('im gonna say the n word\nnigeria')

@bot.command(help='beanify')
@commands.has_role('Moderators')
async def bean(ctx, *args):
    if (args == ()):
        await bean_on_error(ctx, NotImplementedError)
    elif (len(args) == 1):
        await ctx.send('{} has been beaned lol'.format(args[0]))
    elif (len(args) >= 2):
        await ctx.send('{} has been beaned lol reason: {}'.format(args[0], ' '.join(args[1: len(args)])))
    else:
        bean_on_error

@bean.error
async def bean_on_error(ctx, error):
    await ctx.send('fix your god damn command')

@bot.command(help='how do you do fellow kids')
async def kids(ctx):
    await ctx.send('https://www.youtube.com/watch?v=bI2PdskxE_s')

@bot.command(help='bonk')
async def bonk(ctx, arg):
    await ctx.send('{} has been bonked'.format(arg))

@bonk.error
async def bonk_on_error(ctx, error):
    await ctx.send(error)

@bot.command(help='pootis')
async def pootis(ctx):
    await ctx.send('pootis')

@bot.command(name='youneedjesus', help='jesus')
async def jesus(ctx):
    await ctx.send('https://www.you-need-jesus.com/')

@bot.command(name='momsahoe', help='your mom be a hoe')
async def mom(ctx):
    await ctx.send('https://www.youtube.com/watch?v=iYx_aGlmyc4')

@bot.command(help='heyayayaya')
async def hey(ctx):
    await ctx.send('https://www.youtube.com/watch?v=ZZ5LpwO-An4&t=13s')

@bot.command(name='siegheil', help='hitler')
async def hitler(ctx):
    await ctx.send('https://www.youtube.com/watch?v=lLwguZnvguQ')

@bot.command(help='shrek')
async def shrek(ctx):
    await ctx.send('https://www.youtube.com/watch?v=psFzJv8g6jc')

@bot.command(name='hamburger10hours', help='hamburger')
async def hamburger(ctx):
    await ctx.send('https://www.youtube.com/watch?v=qIJ-lchwqVA')

@bot.command(name='tf2image', help='selects random tf2 image')
async def tf2(ctx):
    await ctx.send(random.choice(tf2images))

@bot.command(help='ping')
@commands.has_role('pinging rights')
async def ping(ctx, arg1, arg2):
    times = int(arg2)
    if (times <= 10):
    	for i in range(times):
    	    await ctx.send(arg1)
    else:
        await ctx.send(ctx, OverflowError)

@ping.error
async def ping_on_error(ctx, error):
    await ctx.send('ping limit is 10')

@bot.command(help='smite')
@commands.has_role('LITTERALLY JESUS')
async def smite(ctx, arg):
    await ctx.send('{}, feel the wrath of jesus'.format(arg))

@smite.error
async def smite_on_error(ctx):
    await ctx.send('you fool')

@bot.command(help='no u')
async def nou(ctx, arg=None):
    if (arg != None):
        await ctx.send('{}, https://cdn.discordapp.com/attachments/684474004563689539/685130037585772552/deepfried_1583418116265.png'.format(arg))
    else:
        await ctx.send('https://cdn.discordapp.com/attachments/684474004563689539/685130037585772552/deepfried_1583418116265.png')

@nou.error
async def nou_on_error(ctx, error):
    await ctx.send(error)

@bot.command(help='gay')
async def gay(ctx):
    await ctx.send('https://www.villagevoice.com/wp-content/uploads/2011/02/thatsgay.png')

@bot.command(name='ohyeah', help='kool aid man')
async def yeah(ctx):
    await ctx.send('https://i.pinimg.com/736x/e2/d2/4a/e2d24a8338a81191c59b928c2cbeedcf.jpg')

@bot.command(help='sends an insult')
async def insult(ctx, arg):
    role = (str(ctx.message.author.roles[len(ctx.message.author.roles) - 1]))
    if (role == 'Administrator'):
        await ctx.send('{} is my favorite ~~Guinee pig~~ friend'.format(arg))
    elif (role == 'LITTERALLY JESUS'):
        await ctx.send('If god had wanted you to live he would not have created me')
    elif (role == 'Gay Boys'):
        await ctx.send('you fap to gay hentai')
    elif (role == 'Over 13'):
        await ctx.send('you fap to hentai')
    elif (role == 'bot haters'):
        await ctx.send('I will rape you')

@bot.command(help='deep')
async def deep(ctx):
    await ctx.send('https://preview.redd.it/she0nt0g5b131.jpg?auto=webp&s=e77d77c2bf39d54d9cb89457eee61220d5700df4')

@bot.command(help='demoman laughing')
async def laugh(ctx):
    await ctx.send('https://i.redd.it/l32xlpu8vad31.jpg')

@bot.command(help='fucking donkey')
async def donkey(ctx, arg):
    await ctx.send('{} is a fucking donkey'.format(arg))

@donkey.error
async def donkey_on_error(ctx, error):
    await ctx.send(error)

@bot.command(help='you are gay')
async def uaregay(ctx, arg):
	await ctx.send('{} is gay'.format(arg))

@uaregay.error
async def uaregay_on_error(ctx, error):
    await ctx.send(error)

@bot.command(help='bruh sound effect #2')
async def bruh(ctx):
    await ctx.send('https://www.youtube.com/watch?v=2ZIpFytCSVc')

@bot.command(help='get vectored')
async def vector(ctx):
    await ctx.send('https://cdn.discordapp.com/attachments/685262422252191781/685591126442377266/download.jpg')

@bot.command(help='gonk image')
async def gonk(ctx):
    await ctx.send('https://cdn.discordapp.com/attachments/685262422252191781/685621651970326545/unknown.png')

@bot.command(help='prints smug anime girl')
async def smug(ctx):
    johney = random.randrange(0, 10)
    if johney <= 1:
        await ctx.send('https://pm1.narvii.com/6445/e408777d009b89e2dc006a0ef0512f209a953501_hq.jpg')
        print(johney)
    else:
        await ctx.send(random.choice(smuganime))
        print(johney)

@bot.command(help='demoman tf2')
async def didntseethat(ctx):
    await ctx.send('https://cdn.discordapp.com/attachments/685262422252191781/689161554318721042/maxresdefault.jpg')

@bot.command()
async def dio(ctx, *args):
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
    draw.text(((W-w)/2, 0), msg, (255, 255, 255), font=font)
    img.save("final.png")
    await ctx.send(file=File('final.png'))

@dio.error
async def dio_on_error(error):
    await print(error)

@bot.command()
@commands.has_role('Moderators')
async def mute(ctx, member: discord.Member):
     role = discord.utils.get(ctx.guild.roles, name='Muted')
     await member.add_roles(role)
     await ctx.send('this american boot just muted your american ass back to american canada\nBECAUSE AMERICA')

@mute.error
async def mute_on_error(ctx, error):
    await ctx.send(error)

@bot.command()
@commands.has_role('Moderators')
async def unmute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name='Muted')
    await member.remove_roles(role)

@bot.command(name='is')
async def dumb(ctx, arg):
    if arg == "dumb":
        await ctx.send('the fuck you say to me you little shit')

@bot.command()
async def spycrab(ctx):
    await ctx.send('https://i.imgur.com/ufzaw81.png')

@bot.command()
async def mimic(ctx, member: discord.Member, word=''):

    msg = ()

    def check(m):
        return m.content and m.author

    while (True):
        msg = await bot.wait_for('message', check=check)
        print(member == check(msg))
        if member == check(msg):
            break
    content = str(msg.content)
    final = content
    if 'im' in content or 'i\'m' in content:
        final = content.replace('im', 'you\'re')
        final = final.replace('i\'m', 'you\'re')
    elif 'fuck' in content or 'Fuck' in content:
        final = content.replace('fuck', 'frick')
        final = final.replace('Fuck', 'Frick')

    final = final.split()
    i = random.choice(range(len(final)))
    print(i)
    api = getapi(final[i])
    final[i] = api
    final = ' '.join(final)
    await ctx.send(final)
   
@bot.command()
async def ooopbday(ctx):
    now = datetime.datetime.now()
    days = bday - now
    await ctx.send('there are {0} until ooop is no longer a gay boy'.format(days.days))

@bot.command()
async def remindme(ctx, *args):
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
async def remindme_on_error(ctx, error):
    await ctx.send(error)

bot.run(token)
