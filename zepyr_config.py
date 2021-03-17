from riotwatcher import LolWatcher
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Your LoL region. na1, euw1, eun1, kr, ru..
my_region = "euw1"

# Your riot api key
riot_api_key = os.getenv('RIOT_KEY')

# Your discord token
discord_bot_token = os.getenv('DISCORD_KEY')

# Discord text channel id which you want to post logging to
log_channel_id = 771708479072370698

lol_watcher = LolWatcher(riot_api_key)
latest = lol_watcher.data_dragon.versions_for_region(my_region)[
    'n']['champion']
static_champ_list = lol_watcher.data_dragon.champions(latest, False, 'en_US')
