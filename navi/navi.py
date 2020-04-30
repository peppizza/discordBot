# 'HEY' 'LOOK" "LISTEN" "HEY LISTEN"
#Rules:
#-Hate speech is not allowed.
#-Nothing rude or demeaning should be said to someone, unless the person in question is okay with it. (for instance friends insulting each other back and forth)
#-Refrain from sharing personal information, especially someone else's!
#-Don't harass people. 
#-Don't spam
#-If a mod or admin says not to do something, then you must not do it.
#-If a mod is abusing their power then dm !report to @fellow_kids 
#-Images that may contain gore or other graphic content that is not safe for work are not allowed
#-Threats are not allowed, if for some reason its a joke, then make it clear that there is no ill intentions. (You don't really have to worry about this one most of the time, as it will only be dealt with if a mod or admin sees fit)
#-Self promotion is okay as long as it remains in its respective channel

import os
import secrets
import asyncio
import discord

from discord.ext import commands
from dotenv import load_dotenv

quotes = ['HEY', 'LOOK', 'LISTEN', 'HEY LISTEN']
active = False

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.command()
async def rules(ctx):
    channel = bot.get_channel(704737000078704710)
    embed = discord.Embed(title='Rules', description='-Hate speech is not allowed.\n-Nothing rude or demeaning should be said to someone, unless the person in question is okay with it. (for instance friends insulting each other back and forth)\n-Refrain from sharing personal information, especially someone else\'s!\n-Don\'t harass people. \n-Don\'t spam\n-If a mod or admin says not to do something, then you must not do it.\n-If a mod is abusing their power then dm !report to @fellow_kids \n-Images that may contain gore or other graphic content that is not safe for work are not allowed\n-Threats are not allowed, if for some reason its a joke, then make it clear that there is no ill intentions. (You don\'t really have to worry about this one most of the time, as it will only be dealt with if a mod or admin sees fit)\n-Self promotion is okay as long as it remains in its respective channel')
    await channel.send(embed=embed)

@bot.command(name='start')
@commands.has_role('pinging rights')
async def start(ctx):
    await bot.change_presence(status=discord.Status.online)
    print('commaned recieved')
    await ctx.send('starting...')
    global active
    active = True
    while (active == True):
        await asyncio.sleep(secrets.randbelow(5))
        await ctx.send(secrets.choice(quotes))

@bot.command(name='stop')
@commands.has_role('pinging rights')
async def stop(ctx):
    print('stopping...')
    await ctx.send('stopping...')
    global active
    active = False
    await bot.change_presence(status=discord.Status.idle)

bot.run(token)
