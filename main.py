import discord
from discord.ext import commands
import asyncio
import emoji

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
        name = "{0}avatar".format(bot.command_prefix),
        value = "Returns the avatar of a user.",
        inline = False
    )

    e.add_field(
        name = "{0}say".format(bot.command_prefix),
        value = "Says a custom message provided by the user.",
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

### Run
bot.run(read_token())