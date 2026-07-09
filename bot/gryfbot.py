import os
import discord
from discord.ext import commands
import importlib
import pkgutil

TOKEN = os.getenv("GRYF_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="gryf", intents=intents)

MODULES = {}

def load_modules():
    modules_path = os.path.join(os.path.dirname(__file__), "modules")
    package_name = "bot.modules"

    for loader, module_name, is_pkg in pkgutil.iter_modules([modules_path]):
        full_name = f"{package_name}.{module_name}"
        module = importlib.import_module(full_name)

        if hasattr(module, "run"):
            MODULES[module_name] = module.run
            print(f"[GRYF] Loaded module: {module_name}")
        else:
            print(f"[GRYF] Module {module_name} has no run() function")

load_modules()

@bot.event
async def on_ready():
    print(f"[GRYF] Bot logged in as {bot.user}")

@bot.command()
async def run(ctx, module_name: str):
    """Runs a module from the modules/ folder"""
    if module_name in MODULES:
        await ctx.send(f"Running module: {module_name}")
        result = MODULES[module_name]()
        await ctx.send(f"Result:\n{result}")
    else:
        await ctx.send(f"Module '{module_name}' not found.")

bot.run(TOKEN)
