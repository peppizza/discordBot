import discord
import fellow_kids.discord_ids as const

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        if guild.id != 684472795639447621: return
        new_people = bot.get_channel(const.CHANNEL_NEWPEOPLE)
        rules = bot.get_channel(const.CHANNEL_RULES)
        promotion = bot.get_channel(const.CHANNEL_PROMOTIONS)
        embed = discord.Embed(title='Welcome {}!'.format(member.name), description='Head to {} for the rules,\n{} for self-promotion,\nand feel free to make a suggestion!'.format(rules.mention, promotion.mention))
        await new_people.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        for word in message.content.split():
            word = word.replace('_', '')
            word = word.replace('*', '')
            word = word.replace('~', '')
            word = word.replace('`', '')
            if word.lower() in const.BANNED_WORDS:
                context = await bot.get_context(message=message)
                await self.warn(context, context.author, ('Hate speech'), auto=True)

    @commands.command()
    @commands.has_role(ROLE_MODERATOR)
    async def warn(self, ctx, member: discord.Member, *args, auto=False):
        channel = bot.get_channel(const.CHANNEL_MODERATION)
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