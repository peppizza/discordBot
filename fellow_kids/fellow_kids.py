import os
import discord
import logging
from commandFiles import *

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
    bot.add_cog(moderation.Moderation(bot))
    bot.add_cog(arg_commands.ArgCommands(bot))
    bot.add_cog(dm_commands.DmCommands(bot))
    bot.add_cog(draw_image.DrawImage(bot))
    bot.add_cog(leveling.Leveling(bot))
    bot.add_cog(suggestion_handler.SuggestionHandler(bot))
    bot.add_cog(voice_commands.VoiceCommands(bot))
    bot.run(API_TOKEN)
