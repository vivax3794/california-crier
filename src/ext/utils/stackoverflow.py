import discord
from discord.ext import commands
from loguru import logger


class StackOverflow(commands.Cog):
    """Search the world of StackOverflow!"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def stack(self, ctx, *,search):
        params = {
                "q": search,
                "sort": "relevance",
                "site": "stackoverflow"
                }
        with ctx.typing():
            async with self.bot.http_session.get("https://api.stackexchange.com/2.2/search/advanced", params=params) as resp:
                data = await resp.json()

        if len(data["items"]) == 0:
            await ctx.reply("I am sorry, no response")
        else:
            await ctx.reply(data["items"][0]["link"])


def setup(bot):
    bot.add_cog(StackOverflow(bot))
