import os
import discord
import requests
import json
import random
import text2emotion as te
from replit import db
from keep_alive import keep_alive

client = discord.Client()

starter_motivation = [
  "Cheer Up!!",
  "You can and You will.",
  "You are great.",
  "Everything will be solved."
]

starter_good = [
  "Thats Cool!",
  "Keep going.",
  "Much Appreciated."
]

if ("responding" not in db.keys()):
  db['responding'] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + "\n- " + json_data[0]['a']
  return (quote)
  
def update_motivations(motivating_message):
  if ("motivations" in db.keys()):
    motivations = db['motivations']
    motivations.append(motivating_message)
    db['motivations'] = motivations
  else:
    db['motivations'] = [motivating_message]

def delete_motivation(index):
  motivations = db['motivations']
  if (len(motivations) > index):
    del motivations[index]
    db['motivations'] = motivations

@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
  scores = te.get_emotion(msg)
  
  if msg.startswith('!inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if db['responding']:
    options = starter_motivation
    
    if ('motivations' in db.keys()):
      options = options + list(db['motivations'])

    if ((scores['Sad'] > 0.5) or (scores['Angry'] > 0.5) or (scores['Fear'] > 0.5)):
      await message.channel.send(random.choice(options))

    if ((scores['Happy'] > 0.5) or (scores['Surprise'] > 0.5)):
      await message.channel.send(random.choice(starter_good))

  if (msg.startswith('!new ')):
    motivating_message = msg.split('!new', 1)[1]
    update_motivations(motivating_message)
    await message.channel.send('New Motivating Message added.')

  if (msg.startswith('!del')):
    motivations = []
    if ('motivations' in db.keys()):
      index = int(msg.split('!del', 1)[1])
      delete_motivation(index)
      motivations = db['motivations']
      await message.channel.send(motivations)

  if msg.startswith('!list'):
    motivations = []
    if ('motivations' in db.keys()):
      motivations = db['motivations']
    
    await message.channel.send(motivations)

  if msg.startswith('!responding'):
    value = msg.split('!responding', 1)[1]

    if (value.lower() == True):
      db['responding'] = True
      await message.channel.send('Responding is On.')
    
    else:
      db['responding'] = True
      await message.channel.send('Responding is Off.')

keep_alive()
client.run(os.environ['TOKEN'])
