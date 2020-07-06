import os
import discord
import logging
import sqlite3

from discord.ext import commands
from dotenv import load_dotenv

# https://dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={key}

load_dotenv()
API_TOKEN = os.getenv('DISCORD_TOKEN')

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(messages)s'))
logger.addHandler(handler)

class FellowKids(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix='!', owner_id=253290704384557057, reconnect=True, case_insensitive=False)

    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name='DM me !report to report a user'))

        for file in os.listdir('commands'):
            if  file.endswith('.py'):
                name = file[:-3]
                if name == 'constants': continue
                self.load_extension(f'commands.{name}')


FellowKids().run(API_TOKEN)