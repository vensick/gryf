import discord
from discord.ext import commands
import re
import requests


RAW_URL = "https://raw.githubusercontent.com/vensick/gryf/main/sim/script-br.js"


def load_variant_codes() -> dict[str, str]:
    """Pobiera plik JS z GitHub RAW i wyciąga variantBRcodes."""
    try:
        text = requests.get(RAW_URL, timeout=5).text
    except Exception as e:
        raise RuntimeError(f"Nie udało się pobrać pliku z GitHub RAW: {e}")

    match = re.search(r"const\s+variantBRcodes\s*=\s*\{(?P<body>.*?)\};", text, re.S)
    if not match:
        raise ValueError("Nie znaleziono bloku variantBRcodes w pliku JavaScript")

    body = match.group("body")
    variants: dict[str, str] = {}

    for item in re.finditer(r"([A-Z])\s*:\s*'([^']+)'", body):
        variants[item.group(1)] = item.group(2)

    return variants


def decode_br_codes(code: str) -> list[str]:
    """Dekoduje ciąg BR np. '105115125' → ['10.5', '11.5', '12.5']"""
    values: list[str] = []
    for i in range(0, len(code), 3):
        chunk = code[i:i + 3]
        values.append(f"{int(chunk) / 10:.1f}")
    return values


def build_embed(variant_codes: dict[str, str]) -> discord.Embed:
    embed = discord.Embed(
        title="Battle Ratings",
        color=discord.Color.from_rgb(88, 142, 255)
    )

    for variant in ("A", "B", "C", "D"):
        if variant not in variant_codes:
            continue

        values = decode_br_codes(variant_codes[variant])
        embed.add_field(
            name=f"Wariant {variant}",
            value=" — ".join(values),
            inline=False
        )

    return embed


def setup(bot):
    @bot.command(name="sim")
    async def sim_command(ctx):
        """Wysyła embed BR pobrany z GitHub RAW."""
        try:
            variant_codes = load_variant_codes()
            embed = build_embed(variant_codes)
            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ Błąd SIM: `{e}`")
