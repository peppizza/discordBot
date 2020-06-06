import os
import discord
import logging
from commandFiles import arg_commands
from commandFiles import dm_commands
from commandFiles import draw_image
from commandFiles import leveling
from commandFiles import moderation
from commandFiles import simple_commands
from commandFiles import voice_commands

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

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, arg: str):
        self.bot.reload_extension(arg)

    @commands.command()
    @commands.is_owner()
    async def listExtensions(self, ctx):
        print(self.bot.extensions)

if __name__ == '__main__':
    bot.load_extension('commandFiles.arg_commands')
    bot.add_cog(dm_commands.DmCommands(bot))
    bot.add_cog(draw_image.DrawImage(bot))
    bot.add_cog(leveling.Leveling(bot))
    bot.add_cog(moderation.Moderation(bot))
    bot.add_cog(simple_commands.SimpleCommands(bot))
    bot.add_cog(voice_commands.VoiceCommands(bot))
    bot.add_cog(Admin(bot))
    bot.run(API_TOKEN)
