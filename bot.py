import os
import discord
import responses
import random
from discord import Intents
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()


async def send_message(message, user_message, is_private):
    try:
        response = responses.get_message(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)


def run_bot():
    token = os.getenv('TOKEN')
    server = os.getenv('GUILD')

    intents = discord.Intents.all()
    intents.message_content = True
    intents.members = True

    client = commands.Bot(command_prefix="z.", intents=intents)
    client.remove_command('help')

    @client.event
    async def on_ready():
        for guild in client.guilds:
            if guild.name == server:
                break

        print(f'{client.user} is up and runnin!\n'
              f'{client.user} is connected to the guild:\n'
              f'{guild.name} with id: {guild.id}\n')

        await client.change_presence(
            activity=discord.Activity(type=discord.ActivityType.listening, name="anime openings!"))

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author).split("#")[0]
        channel = str(message.channel.name)
        user_message = str(message.content)

        print(f'{user_message},said by {username} on {channel}')

        if user_message[0] == '*':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)

        elif user_message.lower().startswith('zen'):
            await send_message(message, user_message, is_private=False)

        elif 'happy bday' in user_message.lower() or 'happy birthday' in user_message.lower():
            await send_message(message, user_message, is_private=False)

        bad_words = ["nub", "nudbe", "noob"]

        for word in bad_words:
            if message.content.lower().count(word) > 0:
                print("A bad word was said")
                await message.channel.purge(limit=1)
                await message.channel.send('Kindly, refrain from using bad words!')

        await client.process_commands(message)

    @client.event
    async def on_member_join(member):
        await member.create_dm()
        await member.dm_channel.send(f'Hi {member.name}, welcome to my Discord server!')
        for channel in member.guild.channels:
            if str(channel) == "bot-fire":
                await channel.send(f'Welcome to the server {member.mention}.\n'
                                   'For a list of all the things i can do, type \'z.help\'')

    @client.command()
    async def op(ctx):
        await ctx.send('The One Piece is REAL!!!')

    @client.command()
    async def sasageyo(ctx):
        await ctx.send("Shinzou wo Sasageyou! Devote your hearts!")

    @client.command()
    async def help(ctx):
        await ctx.send('`~In Bot Channel:'
                       '\nUse prefix \'zen\' to ask questions'
                       '\nYou can use \'*zen\' for private replies'
                       '\nTry greeting the bot!'
                       '\nYou can ask some basic questions regarding age and creation'
                       '\n\n~Commands:'
                       '\nz.facts - For interesting facts'
                       '\nz.members - List of all members in the server'
                       '\nTry \'z.op\' and \'z.sasageyo\''
                       '\n\n~Kami-sama Commands:'
                       '\nz.new-channel <name> - Creates new channel with said name'
                       '\nz.del-channel <name> - Deletes existing channel with said name`')

    @client.command(name='facts')
    async def interesting_facts(ctx):
        facts = ['Hot water will turn into ice faster than cold water', 'The Mona Lisa has no eyebrows',
                 'Ants take rest for around 8 Minutes in 12-hour period', 'Coca-Cola was originally green',
                 'A snail can sleep for three years', 'Butterflies taste with their feet',
                 'It is physically impossible for pigs to look up into the sky',
                 'I was created by Master Am20015!', 'You are pretty cute 😉']
        fact = random.choice(facts)
        await ctx.send(fact)

    @client.command(name='members')
    async def mem(ctx):
        for guild in client.guilds:
            if guild.name == server:
                break

        members = '\n - '.join([member.name for member in guild.members])
        await ctx.send(f'Members of the guild are: {members}')

    @client.command(name='new-channel')
    @commands.has_role('Kami-sama')
    async def create_channel(ctx, channel_name):
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if not existing_channel:
            print(f'Creating a new channel: {channel_name}')
            await guild.create_text_channel(channel_name)
            await ctx.send(f'Channel named \'{channel_name}\' has been created successfully')

    @client.command(name='del-channel')
    @commands.has_role('Kami-sama')
    async def delete_channel(ctx, channel_name):
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if existing_channel is not None:
            print(f'Deleting the channel: {channel_name}')
            await existing_channel.delete()
            await ctx.send(f'Channel named \'{channel_name}\' has been deleted successfully')

        else:
            await ctx.send(f'Channel named \'{channel_name}\' does not exist. '
                           f'Enter a valid channel name')

    @client.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send('You do not have the correct role for this command.')

    try:
        client.run(token)
    except discord.errors.HTTPException:
        print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
        os.system('kill 1')
        os.system("python restarter.py")
