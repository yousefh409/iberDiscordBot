import keep_alive

import os
import random

import discord
from dotenv import load_dotenv
import requests
import json
import random


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TWITCH_CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
TWITCH_CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')




awaiting = {} #Of the form {'discord_id': callback}
JOKE_ENDPOINT = "https://sv443.net/jokeapi/v2/joke/Any"
FACT_ENDPOINT = "https://uselessfacts.jsph.pl/random.json?language=en"

EMBED_COLOUR = 1932020

async def help(message):
    em = discord.Embed()
    em.title = "Help"
    em.colour = discord.Colour(EMBED_COLOUR)
    em.type = "rich"
    for key in helpInfo:
        em.add_field(name = key, value = helpInfo[key], inline=False)

    await message.channel.send(embed=em)


async def about(message):
    em = discord.Embed()
    em.title = "About"
    em.colour = discord.Colour(EMBED_COLOUR)
    em.type = "rich"
    em.add_field(name = "What it is", value ="A discord bot for the iber_m8 stream and discord Community", inline=False)
    em.add_field(name="Help Command", value="help", inline=True)
    em.add_field(name="Version", value="1.0.0", inline=True)
    em.add_field(name="Repository", value="https://github.com/yousefh409/iberDiscordBot", inline=False)

    await message.channel.send(embed=em)


async def code(message):
    em = discord.Embed()
    em.title = "Help"
    em.colour = discord.Colour(EMBED_COLOUR)
    em.type = "rich"
    em.add_field(name = "Info", value ="We are an open-source project and would love for you to contribute", inline=False)
    em.add_field(name="Repository", value="https://github.com/yousefh409/iberDiscordBot", inline=False)

    await message.channel.send(embed=em)


async def randomCommand(message):
    contents = message.content.split()
    if len(contents) < 3:
        rand_number = random.randint(0, 1000)
        response = f"here is a random number young padawan: **{rand_number}**"
        await message.channel.send(response)
    elif int(contents[2]) > 0:
        rand_number = random.randint(0, int(contents[2]))
        response = f"here is a random number young padawan: **{rand_number}**"
        await message.channel.send(response)
    else:
        response = f"do not try to fool me"
        await message.channel.send(response)


async def joke(message):
    success, response = make_request(JOKE_ENDPOINT)
    if success:
        if response["type"] == "single":
            joke = response["joke"]
        else:
            joke = response["setup"] + "\n" + response["delivery"]
        response = f"You asked for a joke, **you are getting one**: \n{joke}"
        await message.channel.send(response)
    else:
        response = "we encountered an error with the joke generator :("
        await message.channel.send(response)


async def fact(message):
    success, response = make_request(FACT_ENDPOINT)
    if success:
        fact = response["text"]
        response = f"You asked for a cool fact, **you are getting one** (yes it is true): \n {fact}"
        await message.channel.send(response)
    else:
        response = "we encountered an error with the fact generator :("
        await message.channel.send(response)


async def invite(message):
    em = discord.Embed()
    em.title = "Invite"
    em.colour = discord.Colour(EMBED_COLOUR)
    em.type = "rich"
    em.add_field(name = "iber_m8", value ="Here is the invite link to iber_m8's Discord Server and Community!", inline=False)
    em.add_field(name="Invite", value="https://discord.gg/GNnmW3rbRs", inline=False)

    await message.channel.send(embed=em)


async def live(message):
    access_token = get_access_token()
    url = "https://api.twitch.tv/helix/streams?user_login=iber_m8"
    headers = {"Authorization": f"Bearer {access_token}", "Client-Id": TWITCH_CLIENT_ID}

    success, data = make_request(url, headers=headers)

    em = discord.Embed()
    em.title = "iber_m8"
    em.colour = discord.Colour(EMBED_COLOUR)
    em.type = "rich"
    em.set_author(name="iber_m8", icon_url="https://static-cdn.jtvnw.net/jtv_user_pictures/43df9b86-0775-49d1-a492-c4169b245ce8-profile_image-70x70.png")

    if access_token and success:
        if data['data'] == []:
            em.add_field(name = "Is Live?", value ="Unfortunatley, iber_m8 is not live at the moment, but he will be streaming soon, so see you there when he does!", inline=False)
            await message.channel.send(embed=em)
        else:
            em.add_field(name="Is Live?", value="Yes, iber_m8 is live at the moment! Check him out and make sure to drop a follow.")
            em.add_field(name="Game", value=f"iber_m8 is playing {data['data'][0]['game_name']} at the moment!")
            em.add_field(name="Viewers", value=f"iber_m8 is streaming for {data['data'][0]['viewer_count']} viewers at the moment!")
            await message.channel.send(embed=em)
            await message.channel.send("https://www.twitch.tv/iber_m8")
    else:
        response = "we encountered an error while contacting Twitch :("
        await message.channel.send(embed=em)




def make_request(api_url, func=requests.get, headers={}):

    response = func(url=api_url, headers=headers)

    if response.status_code == 200:
        return True, response.json()

    return False, None


def get_access_token():
    url = f"https://id.twitch.tv/oauth2/token?client_id={TWITCH_CLIENT_ID}&client_secret={TWITCH_CLIENT_SECRET}&grant_type=client_credentials"
    success, data = make_request(url, func=requests.post)

    if success:
        return data["access_token"]
    else:
        return None


commands = {
    'invite': invite,
    'live': live,
    'help': help,
    'about': about,
    'code': code,
    'random': randomCommand,
    'joke': joke,
    'fact': fact,
}

helpInfo = {
    'help': "Gets help(hey, you are reading it now!)",
    'invite': "Gives you the invite link to iber_m8's Discord server!",
    'live': "Tells you whether iber_m8 is live or not, and gives you the stream link if he is!",
    'joke': "Get a random joke(very funny i assure you)",
    'fact': "Get a random cool fact. yes, they are factual",
    'random <(optional)upper>': "Get a random number up to <upper>, which defaults to 1000",
    'about': "Tells you some stuff about the bot",
    'code': "Gives the link to our open-source code, where you can contribute!"
}



@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if str(message.author.id) in awaiting:
        await awaiting[str(message.author.id)](message)
        awaiting.pop(str(message.author.id))
        return

    contents = message.content.split()
    if len(contents) < 1:
        return

    elif len(contents) >= 3 and contents[0] == "iber" and contents[1] == "is" and contents[2] == "bad":
        response = "**banned**"
        await message.channel.send(response)
        return

    elif contents[0] != "!iber":
        return

    if len(contents) <= 1:
        response = "**iber**"
        await message.channel.send(response)

    elif contents[1] in commands:
        await commands[contents[1]](message)


    else:
        response = "I did not understand what you said. Pick up a dictionary young lad"
        await message.channel.send(response)


keep_alive.keep_alive()

client.run(TOKEN)
