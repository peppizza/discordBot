from discord.ext import commands

class DmCommands(commands.Cog):

    def __init__(self, bot):
        """
        Commands that can only be triggered in a DM
        """
        self.bot = bot

    @commands.command()
    @commands.dm_only()
    async def report(self, ctx):
        await ctx.send('https://forms.gle/bwfdc1AyHJ5dL1ZN7')

    @report.error
    async def report_on_error(self, ctx, error):
        await ctx.message.delete()
        await ctx.message.author.send('Please dm me the report command')

def setup(bot):
    bot.add_cog(DmCommands(bot))