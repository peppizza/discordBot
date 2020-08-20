import os
import discord
import logging
import asyncpg

from discord.ext import commands

# https://dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={key}

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

class TokenWasNotFound(Exception):
    def __init__(self):
        """Error raised when the discord api token is not found."""
        super().__init__('The discord api token was not found... the bot will shut down')

if os.environ.get('IS_IN_DOCKER'):
    API_TOKEN = os.getenv('DISCORD_TOKEN')
    POOL_CONFIG = os.getenv('POOL_CONFIG')
    if API_TOKEN is None or POOL_CONFIG is None:
        raise TokenWasNotFound
else:
    from json import load
    with open('config.json', 'r') as in_file:
        config = load(in_file)
        if 'DISCORD_TOKEN' in config and 'POOL_CONFIG' in config:
            API_TOKEN = config['DISCORD_TOKEN']
            POOL_CONFIG = config['POOL_CONFIG']
        else:
            raise TokenWasNotFound


class FellowKids(commands.AutoShardedBot):
    def __init__(self):
        """The main fellow_kids bot class."""
        super().__init__(command_prefix='!', owner_id=253290704384557057, reconnect=True, case_insensitive=False)
        self.loop.create_task(self.async_init())
        self.load_extensions()

    async def async_init(self):
        self.pool = await asyncpg.create_pool(POOL_CONFIG)
        async with self.pool.acquire() as connection:
            connection: asyncpg.Connection
            async with connection.transaction():
                await connection.execute("""
                                    CREATE TABLE IF NOT EXISTS levels(
                                        id BIGINT PRIMARY KEY,
                                        messages INTEGER,
                                        level TEXT
                                    )
                                """)

    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name='How do you do, fellow kids'))

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
        await self.pool.close()


if __name__ == '__main__':
    FellowKids().run(API_TOKEN)
