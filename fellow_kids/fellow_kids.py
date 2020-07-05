import os
import discord
import logging
import sqlite3

from discord.ext import commands
from dotenv import load_dotenv

# https://dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={key}

load_dotenv()
API_TOKEN = os.getenv('DISCORD_TOKEN')

logging.basicConfig(level=logging.INFO)

class FellowKids(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix='!', owner_id=253290704384557057, reconnect=True, case_insensitive=False)

        self.db = sqlite3.connect('settings.db')
        self.cursor = self.db.cursor()

        self.remove_command('help')

    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name='DM me !report to report a user'))

        for file in os.listdir('commands'):
            if  file.endswith('.py'):
                name = file[:-3]
                if name == 'constants': continue
                self.load_extension(f'commands.{name}')


FellowKids().run(API_TOKEN)