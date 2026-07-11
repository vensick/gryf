import discord

def setup(bot):
    @bot.command(name="b")
    async def b_command(ctx):
        """Pokazuje żywotność baz dla wszystkich BR."""

        BASE_HP = {
            1.0: 4000,
            2.3: 6000,
            3.7: 10000,
            5.0: 16000,
            6.7: 22000,
            8.0: 25900,
        }

        embed = discord.Embed(
            title="Żywotność bazy na BR",
            color=discord.Color.from_rgb(88, 142, 255)
        )

        for br, hp in BASE_HP.items():
            embed.add_field(
                name=f"BR {br}",
                value=f"{hp} HP",
                inline=False
            )

        await ctx.send(embed=embed)
