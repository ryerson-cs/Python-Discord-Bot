import discord
from discord.ext import commands
import asyncio
import emoji
import urllib.request
from bs4 import BeautifulSoup
import json
import random
import requests
import re
from random import randint
import urbandictionary
from helpers import *
import time


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

async def find_reddit_link(subreddit, nsfw):
    url = "https://old.reddit.com/r/" + subreddit
    headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.3'}
    try:
        if nsfw:
            sesh = requests.Session()
            sesh.cookies.set(name='over18', value='1', domain='.reddit.com')
            html = sesh.get(url, headers=headers)
            scrapper = BeautifulSoup(html.text,'html.parser')
            table = scrapper.find("div",attrs={'id':'siteTable'})
        else:
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
        name = "{0}insta <<username>>".format(bot.command_prefix),
        value = "Returns the user's Instagram profile and their most recent post.",
        inline = False
    )
    e.add_field(
        name = "{0}ud <<word>>".format(bot.command_prefix),
        value = "Returns definition from Urban Dictionary.", 
        inline = False
    )
    e.add_field(
        name = "{0}pic <<word1,word2,word3...>>".format(bot.command_prefix),
        value = "Returns generated image based on the words provided.", 
        inline = False
    )
    e.add_field(
        name = "{0}define <<word>>".format(bot.command_prefix),
        value = "Returns dictionary definition.",
        inline = False
    )
    e.add_field(
        name = "{0}verbose <<sentence>>".format(bot.command_prefix),
        value = "Changes your sentence words with their synonyms.",
        inline = False
    )
    e.add_field(
        name = "{0}8ball <<sentence>>".format(bot.command_prefix),
        value = "Ask a question and get a random, classic 8ball response.",
        inline = False
    )
    e.add_field(
        name = "{0}inspiro".format(bot.command_prefix),
        value = "A randomly generated inspirational quote generated by an AI.",
        inline = False
    )
    e.add_field(
        name = "{0}pick <<choice 1, choice 2, ..., choice n>>".format(bot.command_prefix),
        value = "Chooses a random item from a given list, delimited by a comma.",
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
    message = message.replace("@", "")

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
async def pic(ctx, *, category):
   
    e = discord.Embed(
        description = f"{ctx.message.author.mention} wanted a picture.",
        color = 0X4259F4
    )
    e.set_image(
        url = requests.get("https://loremflickr.com/600/600/" + category +"/all").url
    )
    e.set_footer(
        text = "Powered by loremflickr.com"
    )

    msg = await ctx.send(embed = e)
    await msg.add_reaction('\N{THUMBS UP SIGN}')
    await msg.add_reaction('\N{THUMBS DOWN SIGN}') 


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
    links = await find_reddit_link(subreddit, nsfw=ctx.channel.is_nsfw())
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
    links = await find_reddit_link(subreddit, nsfw=ctx.channel.is_nsfw())
    randLink = links[random.randint(0, len(links) - 1 )]
    await response.delete()

    if (not type(links) is list):
        await ctx.send("Subreddit is " + links + ".")
        return
    for key, value in randLink.items():
        await ctx.send("__" + key + ":__\n" + value + "\n")
    
@bot.command()
async def ud(ctx, *, definition):
    defs = urbandictionary.define(definition)
    #rand = urbandictionary.random() 
    defs = defs[0:4]
    i = 1
    result = ""
    for d in defs:
        s = d.definition.replace("[", "").replace("]", "").replace("\n", "")
        result += f"{i}) {s}\n"
        i += 1
    
    e = discord.Embed(
        title = "Definiton of " + definition,
        description = result,
        color = 0XFFDF00
    )

    """ 
    Checklist/plans:
        - Incorporate embeded links if they're returned by the API instead of replacing the brackets.
        - Check return type -> if "best def" or by likes
        - Incorporate likes/dislikes
        - Have pages rather than a spillage of definitions, 1 def/page -> might have to write a helper for paging, useful technique
        - Footer will have link to definition page, simply the url
        - Overload such that if nothing is passed in, call the random method
    """
    
    await ctx.send(embed = e)

@bot.command()
async def verbose(ctx, *, sentence):
    reply = await ctx.send("◌ Generating...")
    result = ""
    for word in sentence.lower().split(" "):
        if len(word) <= 3:
            result += word + " "
            continue
        response = requests.get("https://api.datamuse.com/words?ml=" + word)
        data = response.json()
        if len(data) > 0:
            result += data[0]['word'] + " "
            continue
        result += word + " "

    """
    Concerns:
        1) Speed -> Each word needs to pull JSON from site, very time costly and as a result, large sentences take a long while
        2) Might need a dictionary to filter out some common words from getting thesaursed
        3a) Punctuation will ruin the search to empty. "word." -> [] aka no result. Punctuations must be taken out then re-placed after thesaurus.
        3b) Word contractions such as "don't" will ruin uri encode to search up "don%27t" -> "don", wrong word. For whatever reason, the first word returned is "does" which doesn't make sense 
        4) Currently picks the first result which is based on how confident the API is about how similar a word is to query. Playing with query combinations changes results (sometimes drastically).
    """
    await reply.delete()
    await ctx.send(result.capitalize())

@bot.command()
async def define(ctx, *, word):
    result = ""
    title = "Definition for "
    word = re.sub(r"[^a-zA-Z ]", "", word)
    response = requests.get("https://api.datamuse.com/words?sp=" + word + "&md=d")
    data = response.json()
    if len(data) > 0 and 'defs' in data[0]:
        if data[0]['word'] == word.strip():
            title += word
        else:
            title = "Did you mean " + data[0]['word'] + ":"
        df = 1
        for dfn in data[0]['defs']:
            if dfn.startswith("adj", 0, 3):
                result += f"{df}) [Adjective] {dfn[4:].capitalize()}\n"
                df += 1
            if dfn.startswith("adv", 0, 3):
                result += f"{df}) [Adverb] {dfn[4:].capitalize()}\n"
                df += 1
            if dfn.startswith("n", 0, 1):
                result += f"{df}) [Noun] {dfn[2:].capitalize()}\n"
                df += 1
            if dfn.startswith("v", 0, 1):
                result += f"{df}) [Verb] {dfn[2:].capitalize()}\n"
                df += 1
            if dfn.startswith("u", 0, 1):
                result += f"{df}) [Unknown] {dfn[2:].capitalize()}\n"
                df += 1
        e = discord.Embed(
            title = title,
            description = result,
            color = 0X4259F4
        )
        await ctx.send(embed = e)
    else:
        await ctx.send(f"Could not find a definition for {word}.")

@bot.command(name = "8ball")
async def eightball(ctx, *, question):
    response = []
    ## GOOD RESPONSE ##
    response.append(":green_book:|It is certain.|:green_book:")
    response.append(":green_book:|It is decidedly so.|:green_book:")
    response.append(":green_book:|Without a doubt.|:green_book:")
    response.append(":green_book:|Yes, definitely.|:green_book:")
    response.append(":green_book:|You may rely on it.|:green_book:")
    response.append(":green_book:|As I see it, yes.|:green_book:")
    response.append(":green_book:|Most likely.|:green_book:")
    response.append(":green_book:|Outlook good.|:green_book:")
    response.append(":green_book:|Yes.|:green_book:")
    response.append(":green_book:|Signs point to yes.|:green_book:")
    ## UNCERTAIN RESPONSE ##
    response.append(":ledger:|Reply hazy, try again.|:ledger:")
    response.append(":ledger:|Ask again later.|:ledger:")
    response.append(":ledger:|Better not tell you now.|:ledger:")
    response.append(":ledger:|Cannot predict now.|:ledger:")
    response.append(":ledger:|Concentrate and ask again.|:ledger:")
    ## BAD RESPONSE ##
    response.append(":closed_book:|Don't count on it.|:closed_book:")
    response.append(":closed_book:|My reply is no.|:closed_book:")
    response.append(":closed_book:|My sources say no.|:closed_book:")
    response.append(":closed_book:|Outlook not so good.|:closed_book:")
    response.append(":closed_book:|Very doubtful.|:closed_book:")
    await ctx.send(":8ball: {0} :8ball:\n\n{1}".format(question, response[randint(0, len(response)-1)]))

@bot.command()
async def inspiro(ctx):
    e = discord.Embed(
        description = f"{ctx.message.author.mention} needed a little inspiration.",
        color = 0X4259F4
    )
    e.set_image(
        url = requests.get("http://inspirobot.me/api?generate=true").text
    )
    e.set_footer(
        text = "Powered by inspirobot.me"
    )
    await ctx.send(embed = e)

@bot.command()
async def pick(ctx, *, s):
    choices = []
    [choices.append(x.strip()) for x in s.split(",") if x.strip() and x.strip() not in choices]
    if len(choices) == 0:
        await ctx.send("Doesn't look like there were any valid choices.")
    if len(choices) == 1:
        await ctx.send(f"Well, there was only one choice so... I picked {choices[0]}")
    await ctx.send(f"I picked {choices[randint(0, len(choices)-1)]}")

@bot.command()
async def insta(ctx, *, usr):
    url = "https://www.instagram.com/" + usr
    headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.3'}
    sesh = requests.Session()
    html = sesh.get(url, headers=headers)
    scrapper = BeautifulSoup(html.text,'html.parser')
    packet = scrapper.find("body")
    jstr = packet.find("script").string[21:]
    details = [] #a list of stuff we want to pull, in the end, if the list is empty or unexpected length then something went wrong

    try:
        details.append(re.search('\"is_private\":(.+?),', jstr).group(1)) # private boolean
        details.append(re.search('\"profile_pic_url_hd\":\"(.+?)\"', jstr).group(1)) # user profile pic, this is alt, might be better to grab default
        details.append(re.search('\"full_name\":\"(.+?)\"', jstr).group(1)) # full name, different from username. which is same as usr var
        details.append(re.search('\"biography\":\"(.*?)\",', jstr).group(1)) # biography
        details.append(re.search('\"edge_owner_to_timeline_media\":{\"count\":(.+?),', jstr).group(1)) # number of posts
        details.append(re.search('\"edge_followed_by":{\"count\":(.+?)}', jstr).group(1)) # number of followers
        details.append(re.search('\"edge_follow":{\"count\":(.+?)}', jstr).group(1)) # number of followings
        details.append(re.search('\"display_url\":\"(.+?)\"', jstr).group(1)) # first match should return most recent post
        if re.search('\"edge_media_to_caption\":{\"edges\":\[]},', jstr): # try matching empty caption
            details.append("") # if matched append empty
        else:
            details.append(re.search('\"edge_media_to_caption\":{\"edges\":\[{\"node\":{\"text\":\"(.+?)\"', jstr).group(1)) # not empty caption
        details.append(re.search('\"taken_at_timestamp\":(.+?),', jstr).group(1)) # epoch timestamp
        details.append(re.search('\"edge_liked_by\":{\"count\":(.+?)}', jstr).group(1)) # likes
        details.append(re.search('\"edge_media_to_comment\":{\"count\":(.+?)}', jstr).group(1)) # comments
    except AttributeError:
        pass #swallow exception

    if  (len(details) == 0) or (len(details) != 12 and details[0] == 'false' and details[4] != '0'):
        await ctx.send("Seems like the user doesn't exist.")
        return

    e = discord.Embed(
        title = usr,
        description = "{:,}".format(int(details[4])) + " Posts | " + "{:,}".format(int(details[5])) + " Followers | " + "{:,}".format(int(details[6])) + " Following\n[Visit on Instagram](" + url + ")",
        color = 0XF442AA
    )

    if len(details[3]) == 0:
        details[3] = "\u00AD"
    else: 
        details[3] = gstring.correctify(details[3])

    e.add_field(
        name = details[2],
        value = details[3],
        inline = False
    )

    if details[0] == 'false' and details[4] != '0':
        if len(details[8]) == 0:
            details[8] = "\u00AD"
        else: 
            details[8] = gstring.correctify(details[8])

        e.add_field(
            name = "Recent Post: " + time.strftime('%B %d/%y at %I:%M:%S %p', time.localtime(float(details[9]))),
            value = details[8],
            inline = False
        )
        e.set_footer(
            text = "❤️" + "{:,}".format(int(details[10])) + " | 💬" + "{:,}".format(int(details[11])),
        )

        e.set_image(url = details[7])
    elif details[4] == '0':
        e.set_footer(
            text = "User has no posts.",
        )
    else:
        e.set_footer(
            text = "User is private.",
        )
    e.set_thumbnail(url = details[1])

    await ctx.send(embed=e)

@bot.command()
async def test(ctx):
    #don't remove this, this will serve purpose for linking helpers
    await ctx.send(pager.test())

### Run
bot.run(read_token())