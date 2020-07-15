import discord

from discord.ext import commands, menus

class CustomHelpCommand(commands.HelpCommand):
    def get_command_signature(self, command: commands.Command):
        return f'{self.clean_prefix}{command.qualified_name} {command.signature}'

    async def send_bot_help(self, mapping):
        menu = HelpMenu()
        await menu.start(self.context)

class HelpMenu(menus.Menu):
    async def send_initial_message(self, ctx: commands.Context, channel: discord.TextChannel):
        return await channel.send(f'Hello {ctx.author}')

    @menus.button('\N{THUMBS UP SIGN}')
    async def on_thumbs_up(self, payload):
        await self.message.edit(content=f'Got thumbs up from {self.ctx.author}')

class HelpCommandCog(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = CustomHelpCommand()
        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self._original_help_command

def setup(bot):
    bot.add_cog(HelpCommandCog(bot))