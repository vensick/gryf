import os
import discord
from discord.ext import commands
import pkgutil
import importlib

TOKEN = os.getenv("GRYF_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="gryf", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot zalogowany jako {bot.user}")

for module in pkgutil.iter_modules(['bot/commands']):
    importlib.import_module(f"bot.commands.{module.name}").setup(bot)

bot.run(TOKEN)
