import api_static_data
from riotwatcher import ApiError

class Player(object):
    def __init__(self, champion, username, rank, champion_id, user_id):
        self._champion = champion
        self._username = username
        self._userId = user_id
        self._rank = rank
        self._championId = champion_id

    def __repr__(self):
        return str(self._username)

    def __str__(self):
        return str(self._username)

def get_player_object(playerDic):
    return Player(
        champion=get_champion_by_championid(str(playerDic['championId'])),
        username=str(playerDic['summonerName']),
        rank=get_rank_by_summonerid(str(playerDic['summonerId'])),
        champion_id=playerDic['championId'],
        user_id=str(playerDic['summonerId']))


def get_champion_by_championid(champion_id):
    for x, y in api_static_data.static_champ_list['data'].items():
        if(y.get('key') == champion_id):
            return(x)


def get_rank_by_summonerid(summoner_id):
    try:
        league_data = api_static_data.lol_watcher.league.by_summoner(
            api_static_data.my_region, summoner_id)
        for x in league_data:
            if x['queueType'] == 'RANKED_SOLO_5x5':
                chosen_data = x
                return chosen_data['tier'] + " " + chosen_data['rank']
    except ApiError as err:
        if err.response.status_code == 429:
            return "Requests full"
        elif err.response.status_code == 404:
            return "Data not found"
        else:
            return str("Something weird happened with code " + err.response.status_code)


def get_rank_by_summonername(summoner_name):
    try:
        response = api_static_data.lol_watcher.summoner.by_name(
            api_static_data.my_region, summoner_name)
        league_data = api_static_data.lol_watcher.league.by_summoner(
            api_static_data.my_region, response['id'])
        for x in league_data:
            if x['queueType'] == 'RANKED_SOLO_5x5':
                chosen_data = x
                return chosen_data['tier'] + " " + chosen_data['rank']
    except ApiError as err:
        if err.response.status_code == 429:
            return "Requests full"
        elif err.response.status_code == 404:
            return "Data not found"
        else:
            return str("Something weird happened with code " + err.response.status_code)
