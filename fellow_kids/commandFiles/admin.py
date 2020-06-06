from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def reloadExtension(self, ctx, arg: str):
        self.bot.reload_extension('commandFiles.{}'.format(arg))
        await ctx.send('Reloaded extension: commandFiles.{}'.format(arg))

    @reloadExtension.error
    async def reload_extension_on_error(self, ctx, error):
        await ctx.send(error)

    @commands.command()
    @commands.is_owner()
    async def listExtensions(self, ctx):
        await ctx.send(self.bot.extensions)

    @commands.command()
    @commands.is_owner()
    async def loadExtension(self, ctx, arg: str):
        self.bot.load_extension('commandFiles.{}'.format(arg))

    @loadExtension.error
    async def load_extension_on_error(self, ctx, error):
        await ctx.send(error)

def setup(bot):
    bot.add_cog(Admin(bot))