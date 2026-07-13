import discord
from discord.ext import commands
from datetime import datetime, timezone, timedelta

# Stałe rotacji dla aktywności
CYCLE_START = datetime(2026, 7, 13, 0, 0, 0, tzinfo=timezone.utc)
CYCLE_HOURS = 72


def get_next_reset_unix():
    now = datetime.now(timezone.utc)
    hours_since_start = (now - CYCLE_START).total_seconds() / 3600

    # ile pełnych segmentów 72h minęło
    segment = int(hours_since_start // CYCLE_HOURS)

    # początek następnego segmentu
    next_reset_start = CYCLE_START + timedelta(hours=(segment + 1) * CYCLE_HOURS)

    return int(next_reset_start.timestamp())


def build_embed():
    next_reset_unix = get_next_reset_unix()

    embed = discord.Embed(
        title="AKTYWNOŚĆ",
        color=discord.Color.from_rgb(90, 200, 255)
    )

    embed.add_field(
        name="NASTĘPNY RESET:",
        value=f"<t:{next_reset_unix}:R>",
        inline=False
    )

    return embed


def setup(bot):
    @bot.command(name="a")
    async def a_command(ctx):
        try:
            embed = build_embed()
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Błąd A: `{e}`")
