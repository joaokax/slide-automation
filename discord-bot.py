import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import generate_presentation

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)
discord_bot_token = os.getenv("DISCORD_BOT_TOKEN")


@bot.command()
async def presentation(contex):
    await contex.send("Um momento, estou preparando a apresentação...")
    presentation_url = generate_presentation.main()
    await contex.send(contex.author.mention + " aqui está a apresentação da sprint review: " + str(presentation_url))

bot.run(discord_bot_token)

