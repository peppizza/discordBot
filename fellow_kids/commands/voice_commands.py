import discord

class VoiceCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def running(self, ctx):
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('../assets/Why are You Running.mp3'))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    @commands.command()
    async def dead(self, ctx):
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('../assets/Heavy is Dead.mp3'))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
    
    @commands.command()
    async def yankee(self, ctx):
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('../assets/YANKEE WITH NO BRIM.mp3'))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    @commands.command()
    async def jojo(self, ctx):
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('../assets/Goodbye Jojo.mp3'))
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
        self.leaver.start()

    @tasks.loop(minutes=1.0)
    async def leaver(self):
        if self.vc is not None:
            channel = self.vc.channel
            if len(channel.members) == 1:
                await self.vc.disconnect()
                self.leaver.cancel()

    @commands.command()
    async def leave(self, ctx):
        if self.vc is not None: 
            await self.vc.disconnect()
        self.leaver.cancel()