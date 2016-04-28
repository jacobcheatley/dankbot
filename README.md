#Dank Bot

This is a Dank Discord bot made by me for private servers.
Still in active WIP development.

##Features:
 - Lots of modules, including administration, fun, information, replies, tags and more.

##To install:
 - Requires Python 3.5.1
 - Requires [discord.py](https://github.com/Rapptz/discord.py) latest async version and dependencies.
 - Define `DISCORD_TOKEN` as an environment variable, with your bot's token.
 - If you want to use the queries module, define `WOLFRAM_ID` with your Wolfram API ID.
 - Modify the configuration file in cogs/utils/config.py to your settings.

##To run (assuming python points to Python 3.5):
 - `./run_forever.sh` to auto reboot after disconnect.
 - otherwise `python bot.py`
 
##Currently not working:
 - reminders module causes crashes and ends the run loop unexpectedly.