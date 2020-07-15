import discord

from discord.ext import commands, menus

class CustomHelpCommand(commands.HelpCommand):
    def get_command_signature(self, command: commands.Command):
        return f'{self.clean_prefix}{command.qualified_name} {command.signature}'

    async def send_bot_help(self, mapping):
        pages = menus.MenuPages(source=HelpMenuPageOne(range(1, 100)), clear_reactions_after=True)
        await pages.start(self.context)

class HelpMenuPageOne(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=4)

    async def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page
        return '\n'.join(f'{i}. {v}' for i, v in enumerate(entries, start=offset))

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