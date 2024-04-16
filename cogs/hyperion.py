# CronusMainframe/cogs/hyperion.py

import discord
from discord.ext import commands
from discord import app_commands
from utils.scoring_model import calculate_score
from utils.user_data import UserData

class Hyperion(commands.Cog):
    """Scoring system and leaderboard module."""

    def __init__(self, bot):
        self.bot = bot
        self.user_data = UserData('data')

    @commands.Cog.listener()
    async def on_message(self, message):
        """Update user score based on message activity."""
        if message.author.bot:
            return

        self.user_data.on_message(str(message.guild.id), str(message.author.id), bool(message.attachments))

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """Update user score based on forced message deletions."""
        if message.author.bot:
            return

        self.user_data.on_message_delete(str(message.guild.id), str(message.author.id))

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """Update user score based on timeouts."""
        if before.timed_out_until != after.timed_out_until and after.timed_out_until is not None:
            self.user_data.on_member_update(str(after.guild.id), str(after.id), True)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Update user score based on force disconnects."""
        joined_voice = before.channel is None and after.channel is not None
        left_voice = before.channel is not None and after.channel is None
        self.user_data.on_voice_state_update(str(member.guild.id), str(member.id), joined_voice, left_voice)

    @app_commands.command(name='leaderboard', description='Display the leaderboard of user scores')
    async def leaderboard(self, interaction: discord.Interaction):
        """Display the leaderboard of user scores."""
        user_scores = self.user_data.get_user_scores(str(interaction.guild_id))
        sorted_scores = sorted(user_scores.items(), key=lambda x: calculate_score(x[1]), reverse=True)
        leaderboard = []
        for user_id, user_data in sorted_scores[:10]:  # Display top 10 users
            user = await self.bot.fetch_user(int(user_id))
            score = calculate_score(user_data)
            leaderboard.append(f"{user.name}: {score:.2f}")

        embed = discord.Embed(title="Leaderboard", description="\n".join(leaderboard), color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='rank', description='Display the rank and score of the user')
    async def rank(self, interaction: discord.Interaction):
        """Display the rank and score of the user."""
        user_id = str(interaction.user.id)
        user_scores = self.user_data.get_user_scores(str(interaction.guild_id))
        if user_id not in user_scores:
            await interaction.response.send_message("You don't have a score yet.")
            return

        user_data = user_scores[user_id]
        score = calculate_score(user_data)
        sorted_scores = sorted(user_scores.items(), key=lambda x: calculate_score(x[1]), reverse=True)
        rank = sorted_scores.index((user_id, user_data)) + 1

        embed = discord.Embed(title=f"{interaction.user.name}'s Rank", color=discord.Color.blue())
        if interaction.user.avatar:
            embed.set_thumbnail(url=interaction.user.avatar.url)
        embed.add_field(name="Rank", value=str(rank))
        embed.add_field(name="Score", value=f"{score:.2f}")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Hyperion(bot))
