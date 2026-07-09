import discord
from discord.ext import commands
import os

TOKEN = os.getenv("GRYF_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="gryf", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot zalogowany jako {bot.user}")

@bot.command()
async def sim(ctx):
    await ctx.send("Odpalam sim.py...")

    import subprocess
    subprocess.run(["python", "bot/sim.py"])


bot.run(TOKEN)
