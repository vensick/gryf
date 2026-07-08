import discord
from discord.ext import tasks
import os
import datetime

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = 1455886542240350293
MESSAGE_ID = 1524434588745863269

intents = discord.Intents.default()
client = discord.Client(intents=intents)

LETTERS = ["A", "B", "C", "D"]
index = 0  # aktualna litera


def get_next_minute_unix():
    """Zwraca UNIX timestamp za 5 minut"""
    now = datetime.datetime.now()
    next_minute = now + datetime.timedelta(minutes=1)
    return int(next_minute.timestamp())


async def update_embed():
    global index

    # wybierz literę
    letter = LETTERS[index]

    # timestamp za minutę
    next_change_unix = get_next_minute_unix()

    # przygotuj embed
    embed = discord.Embed(
        title="Testowy licznik",
        description=f"Litera: **{letter}**",
        color=0x00ff99
    )

    embed.add_field(
        name="Zmiana za",
        value=f"<t:{next_change_unix}:R>",
        inline=False
    )

    # wyślij aktualizację
    channel = await client.fetch_channel(CHANNEL_ID)
    message = await channel.fetch_message(MESSAGE_ID)
    await message.edit(embed=embed)

    # przejdź do kolejnej litery
    index = (index + 1) % len(LETTERS)


@tasks.loop(minutes=5)
async def minute_update():
    await update_embed()


@client.event
async def on_ready():
    global MESSAGE_ID

    print(f"Zalogowano jako {client.user}")

    channel = await client.fetch_channel(CHANNEL_ID)

    # bot wysyła wiadomość raz
    msg = await channel.send("Tworzę embed…")
    MESSAGE_ID = msg.id

    print("ID nowej wiadomości:", MESSAGE_ID)

    minute_update.start()
    await update_embed()



client.run(TOKEN)
