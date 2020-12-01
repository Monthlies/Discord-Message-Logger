import discord
from discord.ext import commands
from discord.utils import get
from discord import Webhook, AsyncWebhookAdapter
import aiohttp

import json
from datetime import datetime
from datetime import date


intents = discord.Intents.default()
intents.members = True
intents.typing = True
intents.dm_messages = True


def get_hook():
    with open('config.json', 'r') as b:
        return json.loads(b.read())["WebHook"]

def get_token():
    with open('config.json', 'r') as a:
        return json.loads(a.read())["Token"]


def current_time():
    ctime = datetime.now().strftime('%H:%M:%S')
    return ctime


discord_token = get_token()
client = commands.Bot(command_prefix='!')
client.remove_command("help")


@client.event
async def on_ready():
    print(f'Logged in as: {client.user}')


@client.event
async def on_message(message):
    datesent = date.today()
    timesent = current_time()
    if isinstance(message.channel, discord.channel.DMChannel) and message.author != client.user:
        print(f'{datesent} {timesent} | {message.author}: {message.content}')
        file = open("logging.txt", "a")
        file.write(f'{datesent} {timesent} | {message.author}: {message.content}')
        file.write("\n")
        file.close()
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(f'{get_hook()}', adapter=AsyncWebhookAdapter(session))
            embed = discord.Embed(
                color=0xffcdee
            )
            embed.add_field(name='New Message', value=f'{message.content}', inline=False)
            embed.add_field(name='From', value=f'{message.author}', inline=False)
            embed.add_field(name='Time', value=f'{datesent} - {timesent}', inline=False)
            await webhook.send(embed=embed)

    await client.process_commands(message)


client.run(discord_token, bot=False)