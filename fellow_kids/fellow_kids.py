import os
import discord
import logging
import aiosqlite3

from discord.ext import commands
from dotenv import load_dotenv

# https://dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={key}

load_dotenv()
API_TOKEN = os.getenv('DISCORD_TOKEN')

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

class FellowKids(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix='!', owner_id=253290704384557057, reconnect=True, case_insensitive=False)
        self.loop.create_task(self.async_init())
        self.loop.create_task(self.load_extensions())

    async def async_init(self):
        self.db = await aiosqlite3.connect('levels.db')
        self.cursor = await self.db.cursor()

    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name='DM me !report to report a user'))

    async def load_extensions(self):
        await self.wait_until_ready()
        for file in os.listdir('commands'):
            if  file.endswith('.py'):
                name = file[:-3]
                if name == 'constants': continue
                self.load_extension(f'commands.{name}')

    async def close(self):
        await self.db.close()
        await super().close()


FellowKids().run(API_TOKEN)