# CronusMainframe/cogs/themis.py

import re
import discord
from discord.ext import commands
from utils.harmful_keywords import HARMFUL_KEYWORDS

class Themis(commands.Cog):
    """Moderation and rules enforcement module."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """
        Listener for message events to moderate harmful content.
        """
        if message.author == self.bot.user:
            return

        content = message.content.lower()

        # Check for harmful content
        if self.contains_harmful_content(content):
            try:
                await message.delete()
                spoiler_content = "||" + message.content + "||"
                warning_message = f"⚠️ **Warning:** The following message by {message.author.mention} contains potentially harmful content:\n\n{spoiler_content}"
                await message.channel.send(warning_message)
            except discord.errors.Forbidden:
                print(f"Bot does not have permission to delete messages in {message.channel.name}")
            except Exception as e:
                print(f"An error occurred while moderating message: {e}")

    def contains_harmful_content(self, text: str) -> bool:
        """
        Checks if the given text contains harmful content.
        """
        for keyword in HARMFUL_KEYWORDS:
            if re.search(keyword, text, re.IGNORECASE):
                return True

        return False

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def moderate(self, ctx):
        """Command to perform moderation actions."""
        await ctx.send("Performing moderation actions...")

    @moderate.error
    async def moderate_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have the necessary permissions to use this command.")
        else:
            raise error

async def setup(bot):
    await bot.add_cog(Themis(bot))
