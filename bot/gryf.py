import discord
from discord.ext import tasks
import requests
import os

TOKEN = os.getenv("DISCORD_TOKEN")       # ustawić na Render
CHANNEL_ID = 1455886542240350293          # ID kanału
MESSAGE_ID = 1524434588745863269          # ID wiadomości z embedem

GITHUB_FILE_URL = "https://raw.githubusercontent.com/ludwikm/gryf/main/data.json"
# ↑ tu podaj link do pliku, z którego bot ma pobierać dane

intents = discord.Intents.default()
client = discord.Client(intents=intents)

def get_github_data():
    """Pobiera dane z GitHuba"""
    try:
        res = requests.get(GITHUB_FILE_URL)
        return res.text
    except:
        return "Błąd pobierania danych"

async def update_embed():
    """Aktualizuje embed w Discordzie"""
    channel = await client.fetch_channel(CHANNEL_ID)
    message = await channel.fetch_message(MESSAGE_ID)

    data = get_github_data()

    embed = discord.Embed(
        title="Embed",
        description=data,
        color=0x00ff99
    )

    await message.edit(embed=embed)

@tasks.loop(hours=24)
async def daily_update():
    await update_embed()

@client.event
async def on_ready():
    print(f"Zalogowano jako {client.user}")
    daily_update.start()

client.run(TOKEN)
