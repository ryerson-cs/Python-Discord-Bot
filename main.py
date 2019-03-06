import discord

client = discord.Client()

def read_token():
    with open("token.key", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(read_token())
