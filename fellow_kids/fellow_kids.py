import os
import discord
import logging
import aiosqlite3

from dotenv import load_dotenv
from discord.ext import commands

# https://dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={key}

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

load_dotenv()
API_TOKEN = os.getenv('DISCORD_TOKEN')


class FellowKids(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix='!', owner_id=253290704384557057, reconnect=True, case_insensitive=False)
        self.loop.create_task(self.async_init())
        self.load_extensions()

    async def async_init(self):
        self.db = await aiosqlite3.connect('levels.db')
        self.cursor = await self.db.cursor()

    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name='DM me !report to report a user'))

    async def on_message(self, message):
        if message.author.bot: return

        await self.process_commands(message)

    def load_extensions(self):
        for file in os.listdir('commands'):
            if file.endswith('.py'):
                name = file[:-3]
                if name == 'constants': continue
                self.load_extension(f'commands.{name}')

    async def close(self):
        await super().close()
        await self.db.close()


if __name__ == '__main__':
    FellowKids().run(API_TOKEN)
