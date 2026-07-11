import discord

# HP baz dla kluczowych BR
BASE_HP = {
    1.0: 4000,
    2.3: 6000,
    3.7: 10000,
    5.0: 16000,
    6.7: 22000,
    8.0: 25900,
}

# Zakresy BR → klucz tabeli
BR_RANGES = {
    (1.0, 2.0): 1.0,
    (2.3, 3.3): 2.3,
    (3.7, 4.7): 3.7,
    (5.0, 6.3): 5.0,
    (6.7, 7.7): 6.7,
    (7.7, 8.0): 8.0,
}

def map_br(br: float):
    """Mapuje BR do klucza HP."""
    for (low, high), key in BR_RANGES.items():
        if low <= br <= high:
            return key
    if br > 8.0:
        return 8.0
    return None


async def run(ctx, args):
    """
    Moduł GRYF — bomby
    Wywołanie:
        gryfrun bomby
        gryfrun bomby 4.3
    """

    # brak argumentu → pełna tabela
    if len(args) == 0:
        embed = discord.Embed(
            title="Żywotność baz — pełna tabela",
            color=discord.Color.blue()
        )

        for br_key, hp in BASE_HP.items():
            embed.add_field(
                name=f"BR {br_key}",
                value=f"{hp} HP",
                inline=False
            )

        await ctx.send(embed=embed)
        return

    # argument podany → pojedynczy BR
    try:
        br = float(args[0])
    except ValueError:
        await ctx.send("Podano nieprawidłowy BR.")
        return

    mapped = map_br(br)
    if mapped is None:
        await ctx.send("Podano nieprawidłowy BR.")
        return

    hp = BASE_HP[mapped]

    # oblicz uptier
    uptier_br = br + 1.0
    mapped_uptier = map_br(uptier_br)
    hp_uptier = BASE_HP[mapped_uptier]

    embed = discord.Embed(
        title="Żywotność standardowej bazy",
        color=discord.Color.orange()
    )

    embed.add_field(
        name=f"BAZA {br}",
        value=f"**{hp} HP**",
        inline=False
    )

    # uptier tylko jeśli wartość HP jest inna
    if hp_uptier != hp:
        embed.add_field(
            name=f"UPTIER {uptier_br}",
            value=f"**{hp_uptier} HP**",
            inline=False
        )

    await ctx.send(embed=embed)
