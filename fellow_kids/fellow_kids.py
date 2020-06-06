import os
import discord
import logging

from discord.ext import commands
from dotenv import load_dotenv

# https://dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={key}

load_dotenv()
API_TOKEN = os.getenv('DISCORD_TOKEN')

logging.basicConfig(level=logging.INFO)
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='DM me !report to report a user'))

if __name__ == '__main__':
    for file in os.listdir('commandFiles'):
        if file.endswith('.py'):
            name = file[:-3]
            if name == 'constants': continue
            bot.load_extension('commandFiles.{}'.format(name))
    bot.run(API_TOKEN)
