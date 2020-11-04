from riotwatcher import LolWatcher, ApiError
import time
import api_request as api
import asyncio


async def get_win_ratio(summoner_name: str, champion_id: str, lolWatcher: LolWatcher):
    summoner = await api.get_summoner_by_summonername(summoner_name)
    if summoner.response == api.ResType.WAIT:
        asyncio.sleep(summoner.wait_time)
        summoner = await api.get_summoner_by_summonername(summoner_name)
    if(summoner.response == api.ResType.SUCCESS):
        matchlist = await api.get_matchhistory_by_champion(
            summoner.data['accountId'], champion_id)
        if matchlist.response == api.ResType.WAIT:
            asyncio.sleep(matchlist.wait_time)
            matchlist = await api.get_matchhistory_by_champion(matchlist)
        if(matchlist.response != api.ResType.SUCCESS):
            return 'No data'

    wins = 0
    totalMatches = 0
    limit = 21
    for match in matchlist.data['matches']:
        limit -= 1
        if(limit < 0):
            return str(int(wins/totalMatches*100))+"%"

        totalMatches += 1
        gameId = match['gameId']

        match = await api.get_match_by_match_id(gameId)
        if(match.response == api.ResType.WAIT):
            asyncio.sleep(match.wait_time)
            match = await api.get_match_by_match_id(gameId)

        if(match.response == api.ResType.SUCCESS):
            if(check_win(match.data, champion_id) == True):
                wins += 1

    return str(int(wins/totalMatches*100))+"%"


def check_win(new_match: dict, champion_id: str):
    if 'teams' in new_match:
        team1Victory = 'Win' in new_match['teams'][0].get('win')
        playerFound = False
        for x in range(len(new_match['participants'])):
            if(str(champion_id) == str(new_match['participants'][x]['championId'])):
                playerFound = True
                if(str(new_match['participants'][x].get('teamId')) == str(100) and team1Victory == True):
                    return True
                elif(str(new_match['participants'][x].get('teamId')) == str(200) and team1Victory == False):
                    return True
        if playerFound == False:
            print("Player not found")
        return False
    else:
        print("This error shouldn't appear if everything else works")
        return False
