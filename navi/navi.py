# 'HEY' 'LOOK" "LISTEN" "HEY LISTEN"

import os
import random
import time
import asyncio
import discord

from discord.ext import commands
from dotenv import load_dotenv

quotes = ['HEY', 'LOOK', 'LISTEN', 'HEY LISTEN']
global active

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.command(name='start')
@commands.has_role('pinging rights')
async def start(ctx):
    await bot.change_presence(status=discord.Status.online)
    print('commaned recieved')
    await ctx.send('starting...')
    global active
    active = True
    while (active == True):
        await asyncio.sleep(random.randrange(2, 5))
        await ctx.send(random.choice(quotes))

@bot.command(name='stop')
@commands.has_role('pinging rights')
async def stop(ctx):
    print('stopping...')
    await ctx.send('stopping...')
    global active
    active = False
    await bot.change_presence(status=discord.Status.idle)

bot.run(token)
