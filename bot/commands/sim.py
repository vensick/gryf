import discord
from discord.ext import tasks
import os
import datetime

TOKEN = os.getenv("GRYF_TOKEN")
CHANNEL_ID = 1455886542240350293
MESSAGE_ID = None  # bot sam ustawi ID po wysłaniu wiadomości

intents = discord.Intents.default()
client = discord.Client(intents=intents)

LETTERS = ["A", "B", "C", "D"]
index = 0  # aktualna litera


def get_next_minute_unix():
    """Zwraca UNIX timestamp za 1 minutę"""
    now = datetime.datetime.now()
    next_minute = now + datetime.timedelta(minutes=1)
    return int(next_minute.timestamp())


async def update_embed():
    global index, MESSAGE_ID

    # jeśli bot nie ma jeszcze ID wiadomości — nic nie rób
    if MESSAGE_ID is None:
        print("Brak MESSAGE_ID — embed nie może być edytowany.")
        return

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

    # edytuj wiadomość bota
    channel = await client.fetch_channel(CHANNEL_ID)
    message = await channel.fetch_message(MESSAGE_ID)
    await message.edit(embed=embed)

    # przejdź do kolejnej litery
    index = (index + 1) % len(LETTERS)


@tasks.loop(minutes=1)
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

    # start licznika
    minute_update.start()

    # natychmiastowa pierwsza aktualizacja
    await update_embed()


client.run(TOKEN)
