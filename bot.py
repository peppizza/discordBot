import os
import random
import discord.utils

from discord.ext import commands
from dotenv import load_dotenv

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
'https://i.ytimg.com/vi/1a23gJ40Auo/hqdefault.jpg']

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')
client = discord.Client()

@bot.command(name='die', help='kill somone')
async def die(ctx, arg):
    await ctx.send(f'{arg}, kys')

@die.error
async def die_on_error(ctx, error):
    await ctx.send('you fucked up the command you peice of subhuman trash')

@bot.command(name='rr', help='rick roll')
async def rr(ctx):
    await ctx.send('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

@bot.command(name='nword', help='say the n word')
async def nword(ctx):
    await ctx.send('im gonna say the n word\nnigeria')

@bot.command(name='bean', help='beanify')
@commands.has_role('Moderator')
async def bean(ctx, arg, arg2):
    await ctx.send('{} has been beaned lol reason: {}'.format(arg, arg2))

@bean.error
async def bean_on_error(ctx, error):
    await ctx.send('you fucked up the command you peice of subhuman trash')

@bot.command(name='kids', help='how do you do fellow kids')
async def kids(ctx):
    await ctx.send('https://www.youtube.com/watch?v=bI2PdskxE_s')

@bot.command(name='bonk', help='bonk')
async def bonk(ctx, arg):
    await ctx.send('{} has been bonked'.format(arg))

@bonk.error
async def bonk_on_error(ctx, error):
    await ctx.send(error)

@bot.command(name='pootis', help='pootis')
async def pootis(ctx):
    await ctx.send('pootis')

@bot.command(name='youneedjesus', help='jesus')
async def jesus(ctx):
    await ctx.send('https://www.you-need-jesus.com/')

@bot.command(name='momsahoe', help='your mom be a hoe')
async def mom(ctx):
    await ctx.send('https://www.youtube.com/watch?v=iYx_aGlmyc4')

@bot.command(name='hey', help='heyayayaya')
async def hey(ctx):
    await ctx.send('https://www.youtube.com/watch?v=ZZ5LpwO-An4&t=13s')

@bot.command(name='siegheil', help='hitler')
async def hitler(ctx):
    await ctx.send('https://www.youtube.com/watch?v=lLwguZnvguQ')

@bot.command(name='shrek', help='shrek')
async def shrek(ctx):
    await ctx.send('https://www.youtube.com/watch?v=psFzJv8g6jc')

@bot.command(name='hamburger10hours', help='hamburger')
async def hamburger(ctx):
    await ctx.send('https://www.youtube.com/watch?v=qIJ-lchwqVA')

@bot.command(name='tf2image', help='selects random tf2 image')
async def tf2(ctx):
    await ctx.send(random.choice(tf2images))

@bot.command(name='ping', help='ping')
@commands.has_role('Administrator')
async def ping(ctx, arg1, arg2):
    times = int(arg2)
    for i in range(times):
        await ctx.send(arg1)

@ping.error
async def ping_on_error(ctx, error):
    await ctx.send(error)

@bot.command(name='smite', help='smite')
@commands.has_role('LITTERALLY JESUS')
async def smite(ctx, arg):
    await ctx.send('{}, feel the wrath of jesus'.format(arg))

@smite.error
async def smite_on_error(ctx):
    await ctx.send('you fool')

@bot.command(name='nou', help='nou')
async def nou(ctx, arg):
    await ctx.send('{}, no u'.format(arg))

@nou.error
async def nou_on_error(ctx, error):
    await ctx.send(error)

@bot.command(name='gay', help='gay')
async def gay(ctx):
    await ctx.send('https://www.villagevoice.com/wp-content/uploads/2011/02/thatsgay.png')

bot.run(token)