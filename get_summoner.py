import api_static_data
from riotwatcher import ApiError


def GetPlayer(playerDic):
    return Player(
        champion=GetChampion(str(playerDic['championId'])),
        username=str(playerDic['summonerName']),
        rank=GetRankWithId(str(playerDic['summonerId'])),
        championId=playerDic['championId'],
        userId=str(playerDic['summonerId']))


class Player(object):
    def __init__(self, champion, username, rank, championId, userId):
        self._champion = champion
        self._username = username
        self._userId = userId
        self._rank = rank
        self._championId = championId

    def __repr__(self):
        return str(self._username)

    def __str__(self):
        return str(self._username)


def GetChampion(championId):
    for x, y in api_static_data.static_champ_list['data'].items():
        if(y.get('key') == championId):
            return(x)


def GetRankWithId(id):
    try:
        league_data = api_static_data.lol_watcher.league.by_summoner(
            api_static_data.my_region, id)
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


def GetRankWithName(summonerName):
    try:
        response = api_static_data.lol_watcher.summoner.by_name(
            api_static_data.my_region, summonerName)
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
