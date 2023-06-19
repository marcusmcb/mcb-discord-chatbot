import discord
import os
import requests
import json
import random
import re
from decouple import config

# token = os.environ['DISCORD_AUTH_TOKEN']
token = config('DISCORD_AUTH_TOKEN')

def extract_author_name(message):
  pattern = r"name='(.*?)'"
  matches = re.findall(pattern, message)
  if len(matches) >= 2:
    return matches[1]
  return "No author name found"


def generate_random_number():
  return random.randint(1, 100)


def rps_bot_selection():
  rps_options = ['rock', 'paper', 'scissors']
  return random.choice(rps_options)


def get_quote():
  response = requests.get('https://zenquotes.io/api/random/')
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " - " + json_data[0]['a']
  return quote


def get_dadjoke():
  headers = {'Accept': 'application/json'}
  response = requests.get('https://icanhazdadjoke.com/', headers=headers)
  json_response = response.json()
  return json_response['joke']


class DiscordClient(discord.Client):

  async def on_ready(self):
    print('Logged on as', self.user)

  async def on_message(self, message):
    print(message)
    parsed_data = str(message)
    print('--------------')
    username = extract_author_name(parsed_data)

    # don't respond to ourselves
    if message.author == self.user:
      return

    if message.content == '!dadjoke':
      await message.channel.send(get_dadjoke())

    if message.content == '!hello':
      await message.channel.send(f'Hello, {username}!')

    if message.content == '!stella':
      await message.channel.send(
        '--- *** THIS CHANNEL IS NOW IN STELLA MODE *** ---')

    if message.content == '!charlie':
      await message.channel.send(
        '--- *** NEVER FEAR - THE DUCKMAN IS HERE! *** ---')

    if message.content == '!jack':
      await message.channel.send(
        "--- *** WHYYYYYYYYYYYYYYYYYYYYY?????? *** ---")

    if message.content == '!quote':
      quote = get_quote()
      await message.channel.send(quote)

    if message.content == '!bruh':
      await message.channel.send('BRO!')

    if message.content == '!hungry':
      await message.channel.send(
        f"{username} is {generate_random_number()}% hungry right now.")

    if message.content == "!commands":
      await message.channel.send(
        "***BOT COMMANDS:*** enter '!' and any one of the following: charlie, jack, stella, hello, rock, paper, scissors, hungry, duck"
      )

    if message.content == '!duck':
      await message.channel.send(
        "\U0001F986 --- ***QUACK! QUACK!*** --- \U0001F986")

    if message.content in ['!rock', '!paper', '!scissors']:
      rps_response = rps_bot_selection()
      if rps_response == message.content[1:]:
        await message.channel.send(
          f"**Rock Paper Scissors SHOOT!** MCB Chatbot shows {rps_response.upper()} - it's a tie!"
        )
      else:
        win_map = {'rock': 'scissors', 'paper': 'rock', 'scissors': 'paper'}
        if win_map[rps_response] == message.content[1:]:
          await message.channel.send(
            f"**Rock Paper Scissors SHOOT!** MCB Chatbot shows {rps_response.upper()}. Sorry, ***{username}*** but you lose!"
          )
        else:
          await message.channel.send(
            f"**Rock Paper Scissors SHOOT!** MCB Chatbot shows {rps_response.upper()}. ***{username}*** is the winner!"
          )


intents = discord.Intents.default()
intents.message_content = True
client = DiscordClient(intents=intents)
client.run(token)
