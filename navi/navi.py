# 'HEY' 'LOOK" "LISTEN" "HEY LISTEN"

import os
import random
import time

from discord.ext import commands
from dotenv import load_dotenv

quotes = ['HEY', 'LOOK', 'LISTEN', 'HEY LISTEN']

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.command(name='start')
async def start(ctx):
    print('commaned recieved')
    while (True):
        time.sleep(random.randrange(2, 5))
        await ctx.send(random.choice(quotes))

bot.run(token)
