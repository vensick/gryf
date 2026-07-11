import discord
from discord.ext import commands
import re
import requests

# Stałe HP baz dla BR
BASE_HP = {
    1.0: 4000,
    2.3: 6000,
    3.7: 10000,
    5.0: 16000,
    6.7: 22000,
    8.0: 25900,
}

def build_embed():
    """Buduje embed z pełną tabelą HP baz."""
    embed = discord.Embed(
        title="Żywotność baz",
        color=discord.Color.blue()
    )

    for br, hp in BASE_HP.items():
        embed.add_field(
            name=f"BR {br}",
            value=f"{hp} HP",
            inline=False
        )

    return embed

async def bomby_command(ctx, args):
    """Główna funkcja modułu bomby."""
    embed = build_embed()
    await ctx.send(embed=embed)

async def setup(bot):
    """
    Rejestracja modułu GRYF-a — identycznie jak w ec.py.
    """
    bot.add_command_module("bomby", bomby_command)
