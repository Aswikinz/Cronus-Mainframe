# CronusMainframe/bot.py

import os
import logging
import discord
from discord.ext import commands
from discord import app_commands
from config import TOKEN, MODERATOR_ROLE_ID

# Set up logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='logs/bot.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Set up intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# Create bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

# Load cogs
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

@bot.event
async def on_ready():
    await load_extensions()
    await bot.tree.sync()  # Sync slash commands
    logger.info(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

# Error handling
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandNotFound):
        await interaction.response.send_message("Invalid command. Please check the command and try again.")
    elif isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("You don't have the necessary permissions to use this command.")
    else:
        logger.error(f"App Command error: {error}")
        await interaction.response.send_message("An error occurred while executing the command.")

# Run the bot
if __name__ == "__main__":
    bot.moderator_role_id = int(MODERATOR_ROLE_ID)
    bot.run(TOKEN)
