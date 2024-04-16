# Cronus Mainframe Discord Bot

The Cronus Mainframe Discord Bot is designed to enhance the Discord server experience with advanced content moderation, user scoring, and leaderboard functionality, ensuring a safe and engaging community environment.

## Features

- **Themis Module**: Detects and filters harmful content using predefined keywords.
- **Hyperion Module**: Tracks user activity, assigns scores, and manages leaderboards and ranks.
- **Data Persistence**: Stores user data in CSV files to maintain consistency across bot restarts.
- **Slash Commands**: Facilitates interaction through Discord's slash command system.
- **Customization**: Allows server-specific adjustments to the bot’s operations.

## Prerequisites

Ensure the following are installed before setting up the bot:

- Python 3.7 or higher
- discord.py (version 2.0 or higher)
- csv module

Install dependencies with:

```bash
pip install -r requirements.txt
```


## Installation

To install and set up the Cronus Mainframe Discord Bot, follow these steps:

1. Clone the repository:
   
```bash
git clone https://github.com/Aswikinz/Cronus-Mainframe.git
```
2. Navigate to the project directory:
3. Configure the bot:
- Open the `config.py` file and provide the necessary configuration values, such as the Discord bot token and any other required settings.
4. Run the bot:
```bash
python bot.py
```


The bot should now be up and running on your Discord server.

## Usage

To use the Cronus Mainframe Discord Bot, invite it to your Discord server and ensure that it has the necessary permissions to function properly.

Once the bot is online, you can interact with it using the following slash commands:

- `/leaderboard`: Displays the leaderboard of user scores.
- `/rank`: Displays the individual rank and score of the user.

The bot will automatically moderate content and track user activity based on the predefined criteria.

## Configuration

The Cronus Mainframe Discord Bot offers various configuration options to customize its behavior. You can modify the following settings in the `config.py` file:

- `DISCORD_BOT_TOKEN`: The token of your Discord bot.
- `MODERATION_THRESHOLD`: The threshold for triggering content moderation actions.
- `SCORE_WEIGHTS`: The weights assigned to different user activities for score calculation.

Feel free to explore and adjust these settings to suit your server's needs.

## Contributing

Contributions to the Cronus Mainframe Discord Bot are welcome! If you have any ideas, suggestions, or bug reports, please open an issue on the GitHub repository. If you'd like to contribute code, please follow the standard pull request process.

## License

The Cronus Mainframe Discord Bot is released under the MIT License. You are free to use, modify, and distribute the bot in accordance with the terms of the license.

## Support

If you encounter any issues or have questions regarding the Cronus Mainframe Discord Bot, please open an issue on the GitHub repository. We'll be happy to assist you.

## Acknowledgements

We would like to express our gratitude to the following projects and libraries that have made the development of the Cronus Mainframe Discord Bot possible:

- discord.py
- Python

   



