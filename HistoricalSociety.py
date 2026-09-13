import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
import logging
import random


handler = logging.FileHandler(filename='library.log', encoding='utf-8', mode= 'w')
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='-', intents=intents)



#
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Bot Is Online, Synced And Ready To Go {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('hello'):
        await message.channel.send('Hello.')
    await bot.process_commands(message)


@bot.tree.command(name="sum", description="Add's up 2 Numbers (integers)")
@app_commands.describe(left="1st Number", right="2nd Number")
async def sum(interaction: discord.Interaction, left: int, right: int):
    await interaction.response.send_message(left + right)


@bot.tree.command(name="roll", description="Rolls a Dice, Format: NdN")
@app_commands.describe(dice="RollsToPreform d FacesOfDice")
async def roll(interaction: discord.Interaction, dice: str):
    try:
        rolls, limit= map(int, dice.split('d'))
    except Exception:
        await interaction.response.send_message('Wrong Format. To roll a Dice  you need to use NdN (Ex: 2d6)')
        return
    result= ' / '.join(str(random.randint(1, limit)) for r in range(rolls))
    await interaction.response.send_message(f'You rolled : {result}.')


@bot.tree.command(name="decide", description="let Silent Hill Decide Ur Fate.")
@app_commands.describe(choices="Choices You Want me to Decide on. Split them with Comma")
async def decide(interaction: discord.Interaction, choices: str):
    options = [option.strip() for option in choices.split(',')]
    await interaction.response.send_message(f"Silent Hill Has Chosen: {random.choice(options)}")


@bot.tree.command(name="joined", description="Check Joining Date")
@app_commands.describe(member="UserName of Target")
async def joined(interaction: discord.Interaction, member: discord.Member):
    if member.joined_at is None:
        await interaction.response.send_message(f"{member} has no join date[ERROR].")
    else:
        await interaction.response.send_message(f"{member.mention} joined {interaction.guild.name} on {discord.utils.format_dt(member.joined_at, "F")}")


#boot up
bot.run(token, log_handler=handler)