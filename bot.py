import os

import discord
from dotenv import load_dotenv

from commands import evaluate_command

import sessions

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$'):
    await evaluate_command(message)

@client.event
async def on_voice_state_update(member, before, after):
  if not await sessions.check_team(before.channel):
    return

  if len(before.channel.members) == 0:
    await sessions.remove_team(before.channel)

client.run(TOKEN)