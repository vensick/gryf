import discord
from discord.ext import commands
import importlib
import os

class RunCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.modules = {}
        self.load_modules()

    def load_modules(self):
        """Ładuje podmoduły z bot/modules/loader/"""
        base_path = os.path.join(os.path.dirname(__file__), "loader")

        if not os.path.exists(base_path):
            print("[GRYF] Folder loader/ nie istnieje!")
            return

        for file in os.listdir(base_path):
            if file.endswith(".py") and not file.startswith("__"):
                module_name = file[:-3]
                full_import = f"bot.modules.loader.{module_name}"

                try:
                    module = importlib.import_module(full_import)

                    if hasattr(module, "run"):
                        self.modules[module_name] = module.run
                        print(f"[GRYF] Załadowano moduł: {module_name}")
                    else:
                        print(f"[GRYF] Moduł {module_name} nie ma funkcji run()")

                except Exception as e:
                    print(f"[GRYF] Błąd ładowania modułu {module_name}: {e}")

    @commands.command(name="gryfrun")
    async def gryfrun(self, ctx, module_name: str = None, *args):
        """Uruchamia podmoduł GRYF-a"""
        if module_name is None:
            await ctx.send("Podaj nazwę modułu, np. `gryfrun bomby 4.3`")
            return

        if module_name not in self.modules:
            await ctx.send(f"Moduł `{module_name}` nie istnieje w loader/.")
            return

        try:
            await self.modules[module_name](ctx, args)
        except Exception as e:
            await ctx.send(f"Błąd wykonania modułu `{module_name}`: {e}")

async def setup(bot):
    await bot.add_cog(RunCommand(bot))
