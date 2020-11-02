from enum import Enum
from riotwatcher import LolWatcher, ApiError
import api_static_data


api_key = api_static_data.riot_api_key


def GetPlayer(summonerName: str):
    waitTime = 0
    response = ResType.NULL
    try:
        data = api_static_data.lol_watcher.summoner.by_name(
            api_static_data.my_region, summonerName)
        print(data)
        response = ResType.SUCCESS
        return ApiResponse(data, waitTime, response)
    except ApiError as err:
        if err.response.status_code == 429:  # too many requests
            waitTime = err.response.headers['Retry-After']
            response = ResType.WAIT
            return ApiResponse(None, waitTime, response)
        elif err.response.status_code == 404:  # no data
            response = ResType.NODATA
            return ApiResponse(None, waitTime, response)


def GetMatch(summonerId: str):
    # current match
    waitTime = 0
    response = ResType.NULL
    try:
        data = api_static_data.lol_watcher.spectator.by_summoner(
            api_static_data.my_region, summonerId)
        response = ResType.SUCCESS
        return ApiResponse(data, waitTime, response)
    except ApiError as err:
        if err.response.status_code == 429:  # too many requests
            waitTime = err.response.headers['Retry-After']
            response = ResType.WAIT
            return ApiResponse(None, waitTime, response)
        elif err.response.status_code == 404:  # no data
            response = ResType.NODATA
            return ApiResponse(None, waitTime, response)


def GetMatchByMatchId(matchId: str):
    waitTime = 0
    response = ResType.NULL
    try:
        data = api_static_data.lol_watcher.match.by_id(
            api_static_data.my_region, match_id=matchId)
        response = ResType.SUCCESS
        return ApiResponse(data, waitTime, response)
    except ApiError as err:
        print(err)
        if err.response.status_code == 429:  # too many requests
            waitTime = err.response.headers['Retry-After']
            response = ResType.WAIT
            return ApiResponse(None, waitTime, response)
        elif err.response.status_code == 404:  # no data
            response = ResType.NODATA
            return ApiResponse(None, waitTime, response)


def GetSummonerWithName(summonerName):
    waitTime = 0
    response = ResType.NULL
    try:
        data = api_static_data.lol_watcher.summoner.by_name(
            api_static_data.my_region, summonerName)
        response = ResType.SUCCESS
        return ApiResponse(data, waitTime, response)
    except ApiError as err:
        if err.response.status_code == 429:  # too many requests
            waitTime = err.response.headers['Retry-After']
            response = ResType.WAIT
            return ApiResponse(None, waitTime, response)
        elif err.response.status_code == 404:  # no data
            response = ResType.NODATA
            return ApiResponse(None, waitTime, response)


def GetMatchHistoryWithChampion(accountId, championId):
    # use 'accountId' from summoner object
    waitTime = 0
    response = ResType.NULL
    try:
        data = api_static_data.lol_watcher.match.matchlist_by_account(
            region=api_static_data.my_region, encrypted_account_id=accountId, champion=championId)
        response = ResType.SUCCESS
        return ApiResponse(data, waitTime, response)
    except ApiError as err:
        if err.response.status_code == 429:  # too many requests
            waitTime = err.response.headers['Retry-After']
            response = ResType.WAIT
            return ApiResponse(None, waitTime, response)
        elif err.response.status_code == 404:  # no data
            response = ResType.NODATA
            return ApiResponse(None, waitTime, response)


def GetRankWithId(id):
    # use 'id' from summoner object
    waitTime = 0
    response = ResType.NULL
    try:
        data = api_static_data.lol_watcher.league.by_summoner(
            api_static_data.my_region, id)
        for x in data:
            if x['queueType'] == 'RANKED_SOLO_5x5':
                chosen_data = x
                response = ResType.SUCCESS
                return ApiResponse(chosen_data['tier'] + " " + chosen_data['rank'], waitTime, response)
    except ApiError as err:
        if err.response.status_code == 429:  # too many requests
            waitTime = err.response.headers['Retry-After']
            response = ResType.WAIT
            return ApiResponse(None, waitTime, response)
        elif err.response.status_code == 404:  # no data
            response = ResType.NODATA
            return ApiResponse(None, waitTime, response)


class ApiResponse(object):
    def __init__(self, data, waitTime, response: Enum):
        self.data = data
        self.waitTime = waitTime
        self.response = response

    def __repr__(self):
        return str(self.data)

    def __str__(self):
        return str(self.data)


class ResType(Enum):
    NULL = 0
    SUCCESS = 1
    WAIT = 2
    NODATA = 3
