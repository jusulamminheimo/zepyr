# Zepyr

### Building and running
This bot is made with [discord.py](https://github.com/Rapptz/discord.py). For setuping the bot, reference to [quickstart guide](https://discordpy.readthedocs.io/en/latest/quickstart.html).

After setting up the bot, you need to make `api_static_data.py` file to project root, with data:
```
from riotwatcher import LolWatcher

my_region = "euw1"  # Your LoL region. na1, euw1, eun1, kr, ru..
riot_api_key = ''  # Your riot api key
discord_bot_token = '' # Your discord token
log_channel_id = # Discord text channel id which you want to post logging to, type is int

lol_watcher = LolWatcher(riot_api_key)
latest = lol_watcher.data_dragon.versions_for_region(my_region)[
    'n']['champion']
static_champ_list = lol_watcher.data_dragon.champions(latest, False, 'en_US')
```

Run the bot by running `main.py`

### Bot commands
`!game username` - get live game of the user. Also gives winratios of champions on the embed messages. Winratios are calculated in the limits of api key restrictions.

`!rank username` - get soloqueue rank of player
