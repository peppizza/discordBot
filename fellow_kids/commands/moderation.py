import discord
from discord.ext import commands
from .constants import ROLE_MODERATOR, CHANNEL_NEWPEOPLE, CHANNEL_RULES, CHANNEL_PROMOTIONS, CHANNEL_MODERATION, BANNED_WORDS

class Moderation(commands.Cog):

    def __init__(self, bot: commands.AutoShardedBot):
        """Commands meant for moderators."""
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        if guild.id != 684472795639447621: return
        new_people = self.bot.get_channel(CHANNEL_NEWPEOPLE)
        rules = self.bot.get_channel(CHANNEL_RULES)
        promotion = self.bot.get_channel(CHANNEL_PROMOTIONS)
        embed = discord.Embed(title='Welcome {}!'.format(member.name), description='Head to {} for the rules,\n{} for self-promotion,\nand feel free to make a suggestion!'.format(rules.mention, promotion.mention))
        await new_people.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        for word in message.content.split():
            word = word.replace('_', '')
            word = word.replace('*', '')
            word = word.replace('~', '')
            word = word.replace('`', '')
            if word.lower() in BANNED_WORDS:
                context = await self.bot.get_context(message=message)
                await self.warn(context, context.author, ('Hate speech'), auto=True)

    @commands.command(help="Warn someone")
    @commands.has_role(ROLE_MODERATOR)
    async def warn(self, ctx, member: discord.Member, *args, auto=False):
        channel = self.bot.get_channel(CHANNEL_MODERATION)
        await ctx.message.delete()
        embed = discord.Embed(title='WARNING')
        embed.add_field(name='you have been warned by', value=ctx.message.author)
        embed.add_field(name='reason', value=' '.join(args[0:]))
        if not ctx.author.bot:
            await member.send(embed=embed)
        if auto == False:
            embed = discord.Embed(title='{} has been warned'.format(member), description='**{}** has been warned by **{}**'.format(member, ctx.author))
            embed.add_field(name='Reason', value=' '.join(args[0:]))
        else:
            embed = discord.Embed(title='{} has been warned'.format(member), description='**{}** has been automatically warned for hate speech'.format(member))
            embed.add_field(name='original message', value=ctx.message.content)
        await channel.send(embed=embed)

    @warn.error
    async def warn_on_error(self, ctx, error):
        await ctx.message.delete()
        print(error)

    @commands.command(help="Mute a user")
    @commands.has_role(ROLE_MODERATOR)
    async def mute(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name='Muted')
        await member.add_roles(role)
        await ctx.send('this american boot just muted your american ass back to american canada\nBECAUSE AMERICA')

    @mute.error
    async def mute_on_error(self, ctx, error):
        await ctx.send(error)

    @commands.command(help="Unmute a user")
    @commands.has_role(ROLE_MODERATOR)
    async def unmute(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name='Muted')
        await member.remove_roles(role)

def setup(bot):
    bot.add_cog(Moderation(bot))