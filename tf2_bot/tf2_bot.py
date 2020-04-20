import json
import os
import secrets

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='$')

@bot.command()
async def trade(ctx, *args):
    if (args[0] == 'new'):
        await ctx.send('creating new trade...')
        length = 1
        uuid = secrets.randbelow(10000)
        items = []
        value = []
        author = str(ctx.message.author)
        for arg in args:
            if (args[length] == '|'):
                items = args[1:length]
                value = args[length+1:]
            else:
                length = length + 1
        with open('trades.json', 'r+') as infile:
            obj = json.load(infile)
            infile.close()
        with open('trades.json', 'w') as outfile:
            obj[uuid] = [{'items': items, 'value': ''.join(value), 'author': author}]
            json.dump(obj, outfile, indent=4)
            outfile.close()
        await ctx.send('{0} created trade {1} with items: {2} and a value of: {3}'.format(author, uuid, ', '.join(items), ' '.join(value)))
    elif (args[0] == 'remove'):
        with open('trades.json', 'w') as dest_file:
            with open('trades.json', 'r') as source_file:
                for line in source_file:
                    element = json.loads(line.strip())
                    if args[1] in element:
                        del element[args[1]]
                    dest_file.write(json.dumps(element))
            if os.stat('trades.json').st_size == 0:
                dest_file.write("{}")

bot.run(token)
