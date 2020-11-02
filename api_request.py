from enum import Enum
from riotwatcher import LolWatcher, ApiError
import api_static_data


api_key = api_static_data.riot_api_key


def get_player_by_summonername(summoner_name: str):
    wait_time = 0
    response = ResType.NULL
    try:
        data = api_static_data.lol_watcher.summoner.by_name(
            api_static_data.my_region, summoner_name)
        print(data)
        response = ResType.SUCCESS
        return ApiResponse(data, wait_time, response)
    except ApiError as err:
        return get_error_response(err)


def get_live_match_by_summoner_id(summoner_id: str):
    # current match
    wait_time = 0
    response = ResType.NULL
    try:
        data = api_static_data.lol_watcher.spectator.by_summoner(
            api_static_data.my_region, summoner_id)
        response = ResType.SUCCESS
        return ApiResponse(data, wait_time, response)
    except ApiError as err:
        return get_error_response(err)


def get_match_by_match_id(match_id: str):
    wait_time = 0
    response = ResType.NULL
    try:
        data = api_static_data.lol_watcher.match.by_id(
            api_static_data.my_region, match_id=match_id)
        response = ResType.SUCCESS
        return ApiResponse(data, wait_time, response)
    except ApiError as err:
        return get_error_response(err)


def get_summoner_by_summonername(summonerName):
    wait_time = 0
    response = ResType.NULL
    try:
        data = api_static_data.lol_watcher.summoner.by_name(
            api_static_data.my_region, summonerName)
        response = ResType.SUCCESS
        return ApiResponse(data, wait_time, response)
    except ApiError as err:
        return get_error_response(err)


def get_matchhistory_by_champion(account_id, championId):
    # use 'account_id' from summoner object
    wait_time = 0
    response = ResType.NULL
    try:
        data = api_static_data.lol_watcher.match.matchlist_by_account(
            region=api_static_data.my_region, encrypted_account_id=account_id, champion=championId)
        response = ResType.SUCCESS
        return ApiResponse(data, wait_time, response)
    except ApiError as err:
        return get_error_response(err)


def get_rank_with_summonerid(summoner_id):
    # use 'id' from summoner object
    wait_time = 0
    response = ResType.NULL
    try:
        data = api_static_data.lol_watcher.league.by_summoner(
            api_static_data.my_region, summoner_id)
        for x in data:
            if x['queueType'] == 'RANKED_SOLO_5x5':
                chosen_data = x
                response = ResType.SUCCESS
                return ApiResponse(chosen_data['tier'] + " " + chosen_data['rank'], wait_time, response)
    except ApiError as err:
        return get_error_response(err)


def get_error_response(error):
    if error.response.status_code == 429:  # too many requests
        wait_time = error.response.headers['Retry-After']
        response = ResType.WAIT
        return ApiResponse(None, wait_time, response)
    elif error.response.status_code == 404:  # no data
        response = ResType.NODATA
        return ApiResponse(None, 0, response)
    else:  # other error / log entry should be created
        response = ResType.NODATA
        return ApiResponse(None, 0, response)


class ApiResponse(object):
    def __init__(self, data, wait_time, response: Enum):
        self.data = data
        self.wait_time = wait_time
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
