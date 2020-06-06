import discord
from discord.ext import commands
from .constants import THIS_FOLDER

class VoiceCommands(commands.Cog):

    def __init__(self, bot):
        """Any command that uses voice."""
        self.bot = bot

    @commands.command()
    async def running(self, ctx):
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('{}/assets/Why are You Running.mp3'.format(THIS_FOLDER)))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    @commands.command()
    async def dead(self, ctx):
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('{}/assets/Heavy is Dead.mp3'.format(THIS_FOLDER)))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    @commands.command()
    async def yankee(self, ctx):
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('{}/assets/YANKEE WITH NO BRIM.mp3'.format(THIS_FOLDER)))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    @commands.command()
    async def jojo(self, ctx):
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('{}/assets/Goodbye Jojo.mp3'.format(THIS_FOLDER)))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    @running.before_invoke
    @dead.before_invoke
    @yankee.before_invoke
    @jojo.before_invoke
    async def join(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
        self.vc = ctx.voice_client

    @commands.command()
    async def leave(self, ctx):
        if self.vc is not None:
            await self.vc.disconnect()

def setup(bot):
    bot.add_cog(VoiceCommands(bot))