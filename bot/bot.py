import discord
import logging
import os
import random
import json

from discord.ext import commands

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename = 'discord.log', encoding = 'utf-8', mode = 'w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#intents = discord.Intents.default()
#intents.members = True

def get_prefix(client, message):
    with open('/bot/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix)

@client.event
async def on_ready():
    print('Logged on as')
    print('{0.user}'.format(client))
    print(client.user.id)
    print('---------')
# ----------------------------------------------
    print('Servers Connected to: ')
    for guild in client.guilds:
        print('Name: ',guild.name)
        print('ID: ', guild.id)
        print(' ')
        with open('/bot/prefixes.json', 'r') as f:
                prefixes = json.load(f)
        if guild.id not in prefixes:
            prefixes[str(guild.id)] = 'zb!'
                
            with open('/bot/prefixes.json', 'w') as f:
                json.dump(prefixes, f, indent=4)
#-----------------------------------------------
    input_file = open ('/bot/games.json')
    json_array = json.load(input_file)
    discordActivity = []
    range = 0

    for item in json_array:
        activty_list = {'activity':None, 'status':None}
        activty_list['activity'] = item['activity']
        activty_list['status'] = item['status']
        discordActivity.append(activty_list)
        range += 1

    randnumber = random.randrange(0, range)
    discordGame = discord.Game(discordActivity[randnumber]['activity'])
    discordStatus = discord.Status(discordActivity[randnumber]['status'])
    await client.change_presence(status=discordStatus, activity=discordGame)

    print(discordGame, ' ', discordStatus)

@client.event
async def on_guild_join(guild):
    with open('/bot/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = 'zb!'

    with open('/bot/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open('/bot/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('/bot/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@client.command()
async def changeprefix(ctx, prefix):
    with open('/bot/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('/bot/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f'Prefix Changed to: {prefix}')

@client.command()
async def ping(ctx):
    await ctx.send('Pong!')

@client.command(name='99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

token = os.environ.get("DISCORDTOKEN")
client.run(token)