from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        """Commands meant for reloading/loading extensions due to any changes."""
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def reloadextension(self, ctx, arg: str):
        self.bot.reload_extension('commands.{}'.format(arg))
        await ctx.send('Reloaded extension: commands.{}'.format(arg))

    @reloadextension.error
    async def reload_extension_on_error(self, ctx, error):
        await ctx.send(error)

    @commands.command()
    @commands.is_owner()
    async def listextensions(self, ctx):
        await ctx.send(self.bot.extensions)

    @commands.command()
    @commands.is_owner()
    async def loadextension(self, ctx, arg: str):
        self.bot.load_extension('commands.{}'.format(arg))

    @loadextension.error
    async def load_extension_on_error(self, ctx, error):
        await ctx.send(error)

def setup(bot):
    bot.add_cog(Admin(bot))