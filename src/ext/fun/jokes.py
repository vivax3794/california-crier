import discord
from discord.ext import commands
from loguru import logger


JOKE_API = "https://v2.jokeapi.dev/joke/{}?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&format=txt"


class Jokes(commands.Cog):
    """Fun jokes for the hole family"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dadjoke(self, ctx):
        """A classic dad joke."""
        async with self.bot.http_session.get(
                "https://icanhazdadjoke.com/", headers={"Accept": "text/plain", "User-Agent": "California Crier Discord Bot - using AIOHttp. contact: vivax3794@protonmail.com"}
        ) as resp:
            joke = await resp.text()

        await ctx.reply(joke)

    @commands.command(name="programming-joke", aliases=["pro-joke"])
    async def programming_joke(self, ctx):
        """A fun programming joke!"""
        async with self.bot.http_session.get(JOKE_API.format("Programming")) as resp:
            joke = await resp.text()

        await ctx.reply(joke)

    @commands.command()
    async def pun(self, ctx):
        """A fun pun!"""
        async with self.bot.http_session.get(JOKE_API.format("Pun")) as resp:
            joke = await resp.text()

        await ctx.reply(joke)


def setup(bot):
    bot.add_cog(Jokes(bot))
