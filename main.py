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
bot = commands.Bot(command_prefix = "&")
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
    return extracted_records[random.randint(0, len(extracted_records))]
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
async def stop(ctx):
    aID = 161998154881826826
    bID = 142404845234683904
    if ctx.message.author.id == aID or ctx.message.author.id == bID:
        await ctx.send("Bot Stopped :electric_plug:")
        await bot.logout()

@bot.command()
async def reddit(ctx, *, subreddit):
    response = await ctx.send("◌ Collecting...")
    randLink = await find_reddit_link(subreddit)
    await response.delete()

    if(not type(randLink) is dict):
        await ctx.send("Subreddit is " + randLink + ".")
        return
    for key, value in randLink.items():
        await ctx.send("__" + key + ":__\n" + value + "\n")
    
@bot.command()
async def anime(ctx, *, title):
    response = await ctx.send("◌ Hold on...")
    url = "https://twist.moe/a/" + title.lower().strip().replace(" ", "-")
    await response.delete()

    await ctx.send("found " + url)

    """
    driver = webdriver.PhantomJS()
    driver.implicitly_wait(10)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source)
    filename = "testb.txt"
    myfile = open(filename, "w")
    myfile.write(soup.prettify())
    myfile.close()

    
    headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.3'}
    request = urllib.request.Request(url,headers=headers)
    html = urllib.request.urlopen(request).read()
    soup = BeautifulSoup(html, 'html.parser')
    tag=soup.find('video')
    #print(tag) 
    """

### Run
bot.run(read_token())