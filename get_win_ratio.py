from riotwatcher import LolWatcher, ApiError
import time
import api_request as api


def GetWinRatioQuick(summonerName: str, championId: str, lolWatcher: LolWatcher):
    summoner = api.GetSummonerWithName(summonerName)
    if summoner.response == api.ResType.WAIT:
        time.sleep(summoner.waitTime)
        summoner = api.GetSummonerWithName(summonerName)
    if(summoner.response == api.ResType.SUCCESS):
        matchlist = api.GetMatchHistoryWithChampion(
            summoner.data['accountId'], championId)
        if matchlist.response == api.ResType.WAIT:
            time.sleep(matchlist.waitTime)
            matchlist = api.GetMatchHistoryWithChampion(matchlist)
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

        match = api.GetMatchByMatchId(gameId)
        if(match.response == api.ResType.WAIT):
            time.sleep(match.waitTime)
            match = api.GetMatchByMatchId(gameId)

        if(match.response == api.ResType.SUCCESS):
            if(CheckWinQuick(match.data, championId) == True):
                wins += 1

    return str(int(wins/totalMatches*100))+"%"


def CheckWinQuick(newMatch: dict, championId: str):
    if 'teams' in newMatch:
        team1Victory = 'Win' in newMatch['teams'][0].get('win')
        playerFound = False
        for x in range(len(newMatch['participants'])):
            if(str(championId) == str(newMatch['participants'][x]['championId'])):
                playerFound = True
                if(str(newMatch['participants'][x].get('teamId')) == str(100) and team1Victory == True):
                    return True
                elif(str(newMatch['participants'][x].get('teamId')) == str(200) and team1Victory == False):
                    return True
        if playerFound == False:
            print("Player not found")
        return False
    else:
        print("This error shouldn't appear if everything else works")
        return False
