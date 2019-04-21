import discord
from discord.ext import commands
import asyncio
import emoji
import urllib.request
from bs4 import BeautifulSoup
import json
import random



"""bot-env\Scripts\activate.bat"""

### Setup
client = discord.Client()
bot = commands.Bot(command_prefix = "$")
bot.activity = discord.Game("{0}help for commands.".format(bot.command_prefix)) #Please override later
bot.remove_command("help")


### Helpers
def read_token():
    with open("token.key", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

async def find_reddit_link(subreddit):
    url = "https://old.reddit.com/r/" + subreddit
    headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.3'}
    try:    
        request = urllib.request.Request(url,headers=headers)
        html = urllib.request.urlopen(request).read()
        scrapper = BeautifulSoup(html,'html.parser')
        table = scrapper.find("div",attrs={'id':'siteTable'})
    except:
        return "Not Found"

    try:
        links = table.find_all("a",class_="title")
    except:
        return "NSFW"
    extracted_records = []
    for link in links: 
        title = link.text
        url = link['href']
       
        if not url.startswith('http'):
            url = "https://reddit.com"+url 
     
        record = {
            'Title':title,
            'Post':url
            }
        extracted_records.append(record)
    return extracted_records
### Events
@bot.event
async def on_ready():
    print("API Version: {0}".format(discord.__version__))
    print("We have logged in as {0.user}".format(bot))

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(error)

### Commands
@bot.command()
async def help(ctx):
    e = discord.Embed(
        title = "PyBot Commands - Created by Alex Massin & Alex Gomes",
        description = "All available commands provided by PyBot.",
        color = 0XFFDF00
    )
    
    e.set_thumbnail(url = bot.user.avatar_url)
    
    e.add_field(
        name = "{0}ping".format(bot.command_prefix),
        value = "Returns the latency of the bot's response.",
        inline = False
    )

    e.add_field(
        name = "{0}avatar <<user>>".format(bot.command_prefix),
        value = "Returns the avatar of a user.",
        inline = False
    )

    e.add_field(
        name = "{0}say <<message>>".format(bot.command_prefix),
        value = "Says a custom message provided by the user.",
        inline = False
    )

    e.add_field(
        name = "{0}story <<message>>".format(bot.command_prefix),
        value = "Creates custom story out of emojis provided by the user.",
        inline = False
    )
    e.add_field(
        name = "{0}reddit <<subreddit>>".format(bot.command_prefix),
        value = "Generates random post from given subreddit.",
        inline = False
    )
    e.add_field(
        name = "{0}subreddit <<subreddit>>".format(bot.command_prefix),
        value = "Generates top 5 hot posts from given subreddit.",
        inline = False
    )
    e.add_field(
        name = "{0}google <<word>>".format(bot.command_prefix),
        value = "Generates definition from Google.",
        inline = False
    )
    
    await ctx.send(embed = e)


@bot.command()
async def ping(ctx):
    await ctx.send("{0} Pong! {1} ms :ping_pong:".format(ctx.message.author.mention, round(bot.latency * 1000)))

@bot.command()
async def say(ctx):
    message = ctx.message.clean_content[5:]
    await ctx.message.delete()
    await ctx.send(message)

@bot.command()
async def avatar(ctx):
    message = ctx.message.content[10: len(ctx.message.content) -1]
    message = message.replace("!", "")

    if len(message) != 0:
        if (not any(char.isdigit() for char in message) or bot.get_user(int(message)) == None):
            await ctx.send("Please input proper parameters.")
            return 
        username = bot.get_user(int(message)).name
        discrim = bot.get_user(int(message)).discriminator
        avatarURL = bot.get_user(int(message)).avatar_url

    else:
        username = ctx.message.author.name
        discrim = ctx.message.author.discriminator
        avatarURL = ctx.message.author.avatar_url

    e = discord.Embed(
        title = "Avatar for {0}#{1}".format(username, discrim),
        color = 0XFFDF00
    )

    e.set_image(url = avatarURL)
    await ctx.send(embed = e)  

@bot.command()
async def story(ctx, *, story):
    words = story.split(" ")
    result = ""

    for string in words:
        buffer = emoji.emojize(f":{string}:", True)
        if buffer == (f":{string}:"):
            result += buffer.replace(":", "") + " "
        else:    
            result += buffer + " "
    await ctx.send(result)


@bot.command()
async def whois(ctx):
    message = ctx.message.content[9: len(ctx.message.content) -1]
    message = message.replace("!", "")

    if len(message) != 0:
        if (not any(char.isdigit() for char in message) or bot.get_user(int(message)) == None):
            await ctx.send("Please input proper parameters.")
            return 
        username = bot.get_user(int(message)).name
        discrim = bot.get_user(int(message)).discriminator
        avatarURL = bot.get_user(int(message)).avatar_url

    else:
        username = ctx.message.author.name
        discrim = ctx.message.author.discriminator
        avatarURL = ctx.message.author.avatar_url
    
    e = discord.Embed(
        title = "Who is {0}?".format(username),
        color = 0XFFDF00
    )

    e.add_field(
        name = "Discriminator",
        value = discrim,
        inline = False
    )

    e.add_field(
        name = "ID",
        value = message,
        inline = False
    )

    await ctx.send(embed = e)

@bot.command()
async def stop(ctx):
    aID = 161998154881826826
    bID = 142404845234683904
    if ctx.message.author.id == aID or ctx.message.author.id == bID:
        await ctx.send("Bot Stopped :electric_plug:")
        await bot.logout()


@bot.command()
async def subreddit(ctx, *, subreddit):
    response = await ctx.send("◌ Collecting...")
    links = await find_reddit_link(subreddit)
    e = discord.Embed(
        title = "Posts from {0}".format(subreddit),
        description = "Top 5 posts from Hot.",
        color = 0XFFDF00
    )
    
    if(not type(links) is list):
        await ctx.send("Subreddit is " + links + ".")
        return
    for post in links[0: 5]:
        for key, val in post.items():
            e.add_field(
                name = key,
                value = val,
                inline = False
            )
            
    await response.delete()

    await ctx.send(embed = e)



@bot.command()
async def reddit(ctx, *, subreddit):
    response = await ctx.send("◌ Collecting...")
    links = await find_reddit_link(subreddit)
    randLink = links[random.randint(0, len(links) - 1 )]
    await response.delete()

    if(not type(links) is list):
        await ctx.send("Subreddit is " + links + ".")
        return
    for key, value in randLink.items():
        await ctx.send("__" + key + ":__\n" + value + "\n")
    
@bot.command()
async def google(ctx, *, definition):
    response = await ctx.send("◌ Collecting...")
    temp = definition.replace(" ", "%20")
    url = "https://www.google.com/search?q=" + definition + "%20definition"
    headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.3'}
    try:
        request = urllib.request.Request(url,headers=headers)
        html = urllib.request.urlopen(request).read()
        scrapper = BeautifulSoup(html,'html.parser')
        table = scrapper.find("div",attrs={'class':'lr_dct_sf_sen Uekwlc XpoqFe', 'class': 'PNlCoe XpoqFe'})
        links = table.find("span")
    except:
        await ctx.send("Cannot find definition for " + definition)
        return
    await response.delete()
    e = discord.Embed(
        title = "Definiton of " + definition,
        description = str(links)[6:len(str(links)) - 7],
        color = 0XFFDF00
    )
    e.set_footer(
        text="Source: " + url
    )
    await ctx.send(embed = e)


### Run
bot.run(read_token())