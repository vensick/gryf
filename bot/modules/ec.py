import discord
from discord.ext import commands
from datetime import datetime, timezone, timedelta


# Stałe rotacji EC
CYCLE_START = datetime(1970, 1, 1, 8, 0, 0, tzinfo=timezone.utc)
CYCLE_HOURS = 48
VARIANTS = ["A", "B", "C", "D"]


def get_current_variant():
    now = datetime.now(timezone.utc)
    hours_since_start = (now - CYCLE_START).total_seconds() / 3600
    index = int(hours_since_start // CYCLE_HOURS) % 4
    return VARIANTS[index]


def get_next_change_unix():
    now = datetime.now(timezone.utc)
    hours_since_start = (now - CYCLE_START).total_seconds() / 3600

    # ile pełnych segmentów 48h minęło
    segment = int(hours_since_start // CYCLE_HOURS)

    # początek następnego segmentu
    next_segment_start = CYCLE_START + timedelta(hours=(segment + 1) * CYCLE_HOURS)

    return int(next_segment_start.timestamp())


def build_embed():
    variant = get_current_variant()
    next_change_unix = get_next_change_unix()

    embed = discord.Embed(
        title="EC — Rotacja",
        color=discord.Color.from_rgb(255, 200, 90)
    )

    embed.add_field(
        name="Aktualny wariant EC:",
        value=f"**[ {variant} ]**",
        inline=False
    )

    embed.add_field(
        name="Czas do zmiany:",
        value=f"<t:{next_change_unix}:R>",
        inline=False
    )

    return embed


def setup(bot):
    @bot.command(name="ec")
    async def ec_command(ctx):
        try:
            embed = build_embed()
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Błąd EC: `{e}`")
