import discord
import random

from discord.ext import commands

from commandFiles import THIS_FOLDER, ROLE_MODERATOR, CATEGORY_OPENSUGGESTIONS, CATEGORY_CLOSEDSUGGESTIONS, ROLE_EVERYONE, ROLE_BOTDEVELOPER

suggestions = [697102775959552052, 702882611256754289, 702882635365613662, 703312812096749599, 703312842715037766, 703312883055984730, 703312953637863515, 703313003889688696, 703313116154560583]

class SuggestionHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.bannedusers = []

    async def inactivetoopen(self):
        inactivesuggestions = []
        opencategory = self.bot.get_channel(CATEGORY_OPENSUGGESTIONS) 
        if len(opencategory.channels) < 2:
            inactivecategory = self.bot.get_channel(703314675529416785)
            for channels in inactivecategory.channels:
                inactivesuggestions.append(channels.id)
        chosen = random.choice(inactivesuggestions)
        chosen = self.bot.get_channel(chosen)
        await chosen.edit(name='{}-✅'.format(chosen.name).replace('⌛', ''), category=opencategory, sync_permissions=True)
        embed = discord.Embed(title='open', description='This channel is now open for suggestions', color=0x00ff00)
        await chosen.send(embed=embed) 

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in suggestions:
            channel = message.channel
            catagory = channel.category
            if catagory.id == CATEGORY_OPENSUGGESTIONS and message.author.id != 681886537046163506 and message.author.id != 253290704384557057 and message.author.id != 704350265590939649 and not message.author.id in self.bannedusers:
                embed = discord.Embed(title='working on..', description='Your request is now being worked on by the devs', color=0x00ff00)
                category = self.bot.get_channel(CATEGORY_CLOSEDSUGGESTIONS)
                guild = message.guild
                everyone = guild.get_role(ROLE_EVERYONE)
                dev = guild.get_role(ROLE_BOTDEVELOPER)
                await channel.edit(name='{}-⌛'.format((message.channel.name).replace('✅', '')), category=category)
                await channel.set_permissions(message.author, send_messages=True)
                await channel.set_permissions(everyone, send_messages=False)
                await channel.set_permissions(dev, send_messages=True)    
                await channel.send('<@!{}>'.format(253290704384557057), embed=embed)
                await self.inactivetoopen()

    @commands.command(aliases=['done'])
    async def close(self, ctx):
        channel = ctx.message.channel
        category = self.bot.get_channel(703314675529416785)
        embed = discord.Embed(title='inactive', description='this channel is now inactive', color=0x000000)
        await channel.edit(name=str(channel.name).replace('⌛', ''), category=category, sync_permissions=True)
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.has_role(ROLE_MODERATOR)
    async def nosuggest(self, ctx, member: discord.Member):
        self.bannedusers.append(member.id)
    
    @commands.command()
    @commands.has_role(ROLE_MODERATOR)
    async def suggest(self, ctx, member: discord.Member):
        self.bannedusers.remove(member.id)