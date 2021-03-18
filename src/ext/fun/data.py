import io
import time
from collections import defaultdict

import discord
from discord.ext import commands
from loguru import logger
import pandas as pd
from matplotlib import pyplot as plt


class Data(commands.Cog):
    """Fun plots!"""

    def __init__(self, bot):
        self.bot = bot

    async def send_current_plt(self, ctx, *args, **kwargs) -> None:
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        img = discord.File(buf, filename="plot.png")
        await ctx.reply(*args, file=img, **kwargs)
        plt.clf()

    @commands.group(name="plot", invoke_without_command=True)
    async def plot_group(self, ctx):
        plt.plot(range(20))
        await self.send_current_plt(
            ctx,
            "You can use me to get some nice plots for the sever, here is a very simple one.",
        )

    @plot_group.command()
    async def age(self, ctx):
        """Plots the age of users"""
        data = []
        now = time.time()
        for member in ctx.guild.members:
            data.append((member.name, now - time.mktime(member.created_at.timetuple())))

        data.sort(key=lambda x: x[1], reverse=True)
        names = [x[0] for x in data]
        ages = [x[1] / 60 / 60 / 24 / 365 for x in data]
        plt.bar(names, ages)
        if len(data) > 6:
            plt.xticks(ticks=range(0, len(data), len(data) // 6))

        plt.title("age")
        await self.send_current_plt(ctx)

    @plot_group.command()
    async def roles(self, ctx):
        """Plot the different roles."""
        data = defaultdict(int)
        for member in ctx.guild.members:
            highest_role = member.roles[-1]
            data[highest_role] += 1

        roles = []
        ammounts = []
        colors = []
        for role, ammount in data.items():
            roles.append(role.name)
            ammounts.append(ammount)
            color = role.color
            if role.name == "@everyone":
                colors.append((0.5, 0.5, 0.5))
            else:
                colors.append((color.r / 255, color.g / 255, color.b / 255))

        plt.pie(ammounts, labels=roles, colors=colors, autopct="%1.1f%%")
        plt.title("roles")
        plt.axis("equal")
        await self.send_current_plt(ctx)

    @plot_group.command()
    async def status(self, ctx):
        """Plot the different statuses."""
        data = defaultdict(int)
        for member in ctx.guild.members:
            status = member.status
            data[str(status)] += 1

        statues = []
        ammounts = []
        for status, ammount in data.items():
            statues.append(status)
            ammounts.append(ammount)

        plt.pie(ammounts, labels=statues, autopct="%1.1f%%")
        plt.title("status")
        plt.axis("equal")
        await self.send_current_plt(ctx)


def setup(bot):
    bot.add_cog(Data(bot))
