import asyncio
import logging
import os
from typing import Optional

import discord
from discord.ext import commands
from dotenv import load_dotenv

from .commands import BasicCommands
from .auth_commands import AuthCommands
from .storage import ensure_db_exists

log = logging.getLogger("authbot")


def _int_from_env(name: str) -> Optional[int]:
    val = os.getenv(name)
    if not val:
        return None
    try:
        return int(val)
    except ValueError:
        log.warning("Environment var %s is not an integer: %s", name, val)
        return None


def build_bot() -> commands.Bot:
    intents = discord.Intents.default()
    intents.members = True  # required to fetch members and assign roles
    intents.message_content = False  # enable if you need to read message contents

    bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)

    @bot.event
    async def on_ready():
        log.info("Logged in as %s (ID: %s)", bot.user, bot.user.id if bot.user else "?")
        try:
            guild_id = _int_from_env("GUILD_ID")
            if guild_id:
                # Sync commands to a single guild for faster updates during dev
                guild = discord.Object(id=guild_id)
                synced = await bot.tree.sync(guild=guild)
                log.info("Synced %d commands to guild %s", len(synced), guild_id)
            else:
                synced = await bot.tree.sync()
                log.info("Globally synced %d commands", len(synced))
        except Exception:
            log.exception("Failed to sync application commands")

    # Register slash command group
    bot.tree.add_command(BasicCommands())
    bot.tree.add_command(AuthCommands(bot))
    return bot


def run() -> None:
    # Load .env first
    load_dotenv()

    # Basic logging setup
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(level=getattr(logging, level, logging.INFO), format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    # Ensure data.json exists
    ensure_db_exists()

    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("DISCORD_TOKEN is not set. Create a .env file or export the environment variable.")

    bot = build_bot()
    bot.run(token)
