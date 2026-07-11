import discord
from discord.ext import commands

class Bomby(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.base_hp = {
            1.0: 4000,
            2.3: 6000,
            3.7: 10000,
            5.0: 16000,
            6.7: 22000,
            8.0: 25900,
        }

        # Zakresy BR → klucz tabeli
        self.br_ranges = {
            (1.0, 2.0): 1.0,
            (2.3, 3.3): 2.3,
            (3.7, 4.7): 3.7,
            (5.0, 6.3): 5.0,
            (6.7, 7.7): 6.7,
        }

    def map_br(self, br):
        for (low, high), key in self.br_ranges.items():
            if low <= br <= high:
                return key
        if br > 8.0:
            return 8.0
        return None

    @commands.command(name="gryfbomby")
    async def gryfbomby(self, ctx, br: float = None):
        # brak argumentu → pełna tabela
        if br is None:
            embed = discord.Embed(
                title="Żywotność baz dla wszystkich BR",
                color=discord.Color.blue()
            )
            for br_key, hp in self.base_hp.items():
                embed.add_field(
                    name=f"BR {br_key}",
                    value=f"{hp} HP",
                    inline=False
                )
            await ctx.send(embed=embed)
            return

        # argument podany → pojedynczy BR
        mapped = self.map_br(br)
        if mapped is None:
            await ctx.send("Podano nieprawidłowy BR.")
            return

        hp = self.base_hp[mapped]

        # oblicz uptier
        uptier_br = br + 1.0
        mapped_uptier = self.map_br(uptier_br)
        hp_uptier = self.base_hp[mapped_uptier]

        embed = discord.Embed(
            title=f"Żywotność standardowej bazy",
            color=discord.Color.orange()
        )

        embed.add_field(
            name=f"BAZA {br}",
            value=f"**{hp} HP**",
            inline=False
        )

        # uptier tylko jeśli wartość jest inna
        if hp_uptier != hp:
            embed.add_field(
                name=f"UPTIER {br + 1.0}",
                value=f"**{hp_uptier} HP**",
                inline=False
            )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Bomby(bot))
