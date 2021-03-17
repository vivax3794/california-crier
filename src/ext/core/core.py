from discord.ext import commands
from loguru import logger


class Core(commands.Cog):
    """Core bot commands."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def alive(self, ctx):
        """"Test that the bot is alive."""
        await ctx.reply("yes I am alive, thanks for checking in on me :D")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def close(self, ctx):
        """Stop the bot"""
        await ctx.reply("good bye!")
        await self.bot.close()


def setup(bot):
    bot.add_cog(Core(bot))
