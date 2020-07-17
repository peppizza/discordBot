import discord
import wavelink
from discord.ext import commands

class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, 'wavelink'):
            self.bot.wavelink = wavelink.Client(bot=self.bot)

        self.bot.loop.create_task(self.start_nodes())

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        # Initiate our nodes. For this example we will use one server.
        # Region should be a discord.py guild.region e.g sydney or us_central (Though this is not technically required)
        await self.bot.wavelink.initiate_node(host='127.0.0.1',
                                              port=2333,
                                              rest_uri='http://127.0.0.1:2333',
                                              password='youshallnotpass',
                                              identifier='TEST',
                                              region='us_central')

    @commands.command(name='connect')
    async def connect_(self, ctx, *, channel: discord.VoiceChannel=None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise discord.DiscordException('No channel to join. Please either specify a valid channel or join one.')

        player = self.bot.wavelink.get_player(ctx.guild.id)
        await ctx.send(f'Connecting to **`{channel.name}`**')
        await player.connect(channel.id)

    @commands.command(aliases=['p'])
    async def play(self, ctx, *, query: str):
        tracks = await self.bot.wavelink.get_tracks(f'ytsearch:{query}')

        if not tracks:
            return await ctx.send('Could not find any songs with that query.')

        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.invoke(self.connect_)

        await ctx.send(f'Added {str(tracks[0])} to the queue.')
        await player.play(tracks[0])

    @commands.command(aliases=['dc'])
    async def disconnect(self, ctx):
        player: wavelink.Player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            return await ctx.send('The bot is not in a voice channel')

        await player.stop()
        await player.disconnect()

    @commands.command(aliases=['c'])
    async def clear(self, ctx):
        player: wavelink.Player = self.bot.wavelink.get_player(ctx.guild.id)

        await player.stop()

    @commands.command()
    async def pause(self, ctx):
        player: wavelink.Player = self.bot.wavelink.get_player(ctx.guild.id)

        if player.is_paused:
            await ctx.send('The player is already paused')
        else:
            await player.set_pause(True)

    @commands.command()
    async def unpause(self, ctx):
        player: wavelink.Player = self.bot.wavelink.get_player(ctx.guild.id)

        if not player.is_paused:
            await ctx.send('The player is already playing')
        else:
            await player.set_pause(False)

    @commands.command()
    async def volume(self, ctx, *, level: int):
        if level < 0 or level > 100:
            return await ctx.send('Please select a value from 1 to 100')
        player: wavelink.Player = self.bot.wavelink.get_player(ctx.guild.id)

        await player.set_volume(level)
    
    @commands.command()
    async def np(self, ctx):
        player: wavelink.Player = self.bot.wavelink.get_player(ctx.guild.id)

        embed = discord.Embed(title='Now playing', description=player.current.title)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Music(bot))