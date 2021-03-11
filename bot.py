#discord_bot.py
'''
GOAL FUNCTIONALITY:
 - notify when a new bill or vote happens
 - ask for latest bills
 - look up stats
    - who authors/seconds the most
    - what's the most controversial bills
 - look up more info about a bill
 - look up stats about a senator 
'''

import os
import asyncio
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
import datetime as dt

import asuciasuci as asuci

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name} (ID: {client.user.id})")

@client.event
async def on_message(mssg):
    if mssg.author == client.user: pass
    elif mssg.content.startswith(',new_bills_today') or mssg.content.startswith(',,nbt'):
        b, d = asuci.get_new_bills() # bill is all bills, d is list of ids for changed bills

        for ID in d:
            for bill in b:
                if bill.get('id') == ID:
                    embd = asuci.bill_template(bill)
                    await mssg.channel.send(embed = embd)

@tasks.loop(hours=1.5708)                     
async def background_task():
    pass

client.loop.create_task(background_task())
client.run(TOKEN)