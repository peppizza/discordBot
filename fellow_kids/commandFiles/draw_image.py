import os
from PIL import Image, ImageFont, ImageDraw
from discord import File
from discord.ext import commands
from commandFiles import THIS_FOLDER, BANNED_WORDS

class DrawImage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dio(self, ctx, *args):
        if self.filter(' '.join(args[:])):
            return
        W = 1280
        msg = ' '.join(args[:]).upper()
        if len(msg) <= 18:
            fontSize = 144
        elif len(msg) <= 25:
            fontSize = 100
        elif len(msg) <= 30:
            fontSize = 70
        else:
            fontSize = 50

        font = ImageFont.truetype("/usr/share/fonts/truetype/msttcorefonts/Impact.ttf", fontSize)
        await self.drawText(ctx, msg, font, W, '{}/assets/dio.jpg'.format(THIS_FOLDER))

    # @commands.command()
    # async def line(self, ctx, *args):
    #     if self.filter(' '.join(args[:]))

    async def drawText(self, ctx, text, font, W, image):
        img = Image.open(image)
        draw = ImageDraw.Draw(img)
        w = draw.textsize(text, font=font)[0]
        async with ctx.typing():
            draw.text(((W-w)/2, 0), text, (255, 255, 255), font=font)
            img.save('{}/assets/final.png'.format(THIS_FOLDER))
            await ctx.send(file=File('{}/assets/final.png'.format(THIS_FOLDER)))

    def filter(self, text):
        text = text.replace('_', '')
        text = text.replace('*', '')
        text = text.replace('~', '')
        text = text.replace('`', '')
        for word in text.split():
            if word.lower() in BANNED_WORDS:
                return True

        return False