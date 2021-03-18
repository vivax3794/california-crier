import os

import discord
from discord.ext import commands
from loguru import logger
import aiohttp
from cogwatch import watch

from . import constants


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=constants.PREFIX, intents=discord.Intents.all())
        self.load_extensions()
        self.http_session = aiohttp.ClientSession()

    def load_extensions(self):
        for ext in constants.EXTENSION_PATH.glob("*/[!_]*.py"):
            dot_path = str(ext).replace(os.sep, ".")[:-3]
            self.load_extension(dot_path)
            logger.info(f"loaded: {dot_path}")

    def run(self) -> None:
        super().run(constants.TOKEN)

    @watch(path="src/ext")
    async def on_ready(self):
        logger.info("bot online")

    async def close(self):
        await self.http_session.close()
        await super().close()
