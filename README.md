# asuci_discord
A discord bot to send updates when an ASUCI (the student senate of UCI) bill is voted on, presented, or overturned to a Discord community

## Functionality
 - regularly checks if there's a new bill or change in status for bills on [this page]("https://www.asuci.uci.edu/senate/legislation/")
 - it scrapes the page using beautiful soup and selenium since the page is dynamically generated every time it's loaded
 - you can set how frequently it checks for updates (defaults to every 2.5 hours) 

### Commands
 - `,new_bills_today` / `,,nbt`: checks if there's any new bills presented, voted on, or overturned on the date the command was issued (PST)

## Docs
### Libraries used:
 - Selenium with Python: for getting page sources for non-static webpages
 - Beautiful Soup 4: for web scraping page sources
 - Discord.py: for running the discord bot

### Repo
 - `asuciasuci.py` is the main program
 - `utils.py` contains a few helper functions for `asuciasuci.py`
 - `discord_bot.py` runs the bot and calls functions from `asuciasuci.py`
 - `.env` should be filled out with the private bot token as such: 
```
# .env
DISCORD_TOKEN=<insert token here w no angle brackets>
```

## To-do
