import asyncio

import discord
from discord.ext import commands as discord_commands
from twitchio.ext import commands as twitch_commands
from loguru import logger

from ... import constants


class TwitchBot(twitch_commands.Bot):
    def __init__(self, discord_cog: "DiscordCog"):
        super().__init__(
            irc_token=constants.TWITCH_TOKEN,
            initial_channels=[constants.TWITCH_CHANNEL],
            nick="therealvivax",
            prefix="asfnaosidjdosa",
        )
        self.discord_cog = discord_cog
        self.is_ready = False

    async def event_ready(self):
        self.is_ready = True

    async def ready(self):
        await self._ws.send_privmsg(
            constants.TWITCH_CHANNEL, "discord - twitch bridge online."
        )

    async def on_discord_msg(self, author: str, msg: str):
        await self._ws.send_privmsg(constants.TWITCH_CHANNEL, f"{author}: {msg}")

    async def event_message(self, message):
        if message.author.name.lower() == "therealvivax":
            return

        await self.discord_cog.on_twitch_msg(message.author.name, message.content)


class DiscordCog(discord_commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord_commands.Cog.listener()
    async def on_ready(self):
        await self.setup_twitch()
        await self.setup_discord()

        while not self.twitch_bot.is_ready:
            await asyncio.sleep(0.1)

        logger.info("bridge ready")
        await self.twitch_bot.ready()
        await self.webhook.send("twitch - discord bridge online")

    async def setup_twitch(self):
        self.twitch_bot = TwitchBot(self)
        logger.info("twitch bot starting")
        self.twitch_task = asyncio.create_task(self.twitch_bot.start())

    async def setup_discord(self):
        self.channel = self.bot.get_channel(constants.TWITCH_DISCORD_CHANNEL)
        webhooks = await self.channel.webhooks()
        if len(webhooks) > 1:
            logger.warning("more than one webhook found, using first one")
            self.webhook = webhooks[0]
        elif len(webhooks) == 1:
            self.webhook = webhooks[0]
        else:
            logger.warning("creating new webhook")
            self.webhook = await self.channel.create_webhook(
                name="twitch", reason="twitch - discord bridge"
            )

    def cog_unload(self):
        logger.info("closing twitch")
        self.twitch_task.cancle()

    async def on_twitch_msg(self, author: str, msg: str) -> None:
        await self.webhook.send(msg, username=author)

    @discord_commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.channel != self.channel or message.webhook_id is not None:
            return

        await self.twitch_bot.on_discord_msg(message.author.name, message.content)


def setup(bot):
    if constants.BRIDGE:
        bot.add_cog(DiscordCog(bot))
        logger.info("added cog twitch-bridge")
    else:
        logger.warning("bridge not on")
