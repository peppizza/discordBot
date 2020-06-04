import os
import discord
import logging

from fellow_kids.moderation import Moderation
from fellow_kids.image_draw import ImageDraw
from fellow_kids.image_draw import Leveling
from fellow_kids.suggestion_handler import SuggestionHandler

# there gotta be a better way to do this
from fellow_kids.commands import SimpleCommands
from fellow_kids.commands import ArgCommands
from fellow_kids.commands import DmCommands
from fellow_kids.commands import VoiceCommands

from discord.ext import tasks, commands
from discord import File
from dotenv import load_dotenv

# https://dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={key}

load_dotenv()
API_TOKEN = os.getenv('DISCORD_TOKEN')
API_KEY = os.getenv('API_KEY')

logging.basicConfig(level=logging.INFO)
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='DM me !report to report a user'))

if __name__ == '__main__':
    bot.add_cog(SuggestionHandler(bot))
    bot.add_cog(ArgCommands(bot))
    bot.add_cog(SimpleCommands(bot))
    bot.add_cog(DmCommands(bot))
    bot.add_cog(VoiceCommands(bot))
    bot.add_cog(Moderation(bot))
    bot.add_cog(Leveling(bot))
    bot.add_cog(ImageDraw(bot))
    bot.run(API_TOKEN)
