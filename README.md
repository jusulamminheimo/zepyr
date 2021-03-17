# Zepyr

Zepyr is a Discord bot made for pulling and showing data from [Riot Games API](https://developer.riotgames.com/apis).

### Building and running

This bot is made with [discord.py](https://github.com/Rapptz/discord.py). For setuping the bot, reference to [quickstart guide](https://discordpy.readthedocs.io/en/latest/quickstart.html).

After setting up the bot, you need to edit `config_file.py` file to project root, with your own keys & channel id.

Run the bot by running `main.py`

### Bot commands

`!game username` - get live game of the user. Also gives winratios of champions on the embed messages. Winratios are calculated in the limits of api key restrictions.

`!rank username` - get soloqueue rank of player
