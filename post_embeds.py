from logging import error
from discord import player
from riotwatcher import LolWatcher, ApiError
import discord
import get_win_ratio
import api_static_data
import time
import get_summoner
import api_request as api


baseUrl = "https://static.wikia.nocookie.net/leagueoflegends/images/"
rankIconIron = baseUrl + "0/03/Season_2019_-_Iron_1.png"
rankIconBronze = baseUrl + "f/f4/Season_2019_-_Bronze_1.png"
rankIconSilver = baseUrl + "7/70/Season_2019_-_Silver_1.png"
rankIconGold = baseUrl + "9/96/Season_2019_-_Gold_1.png"
rankIconPlatinum = baseUrl + "7/74/Season_2019_-_Platinum_1.png"
rankIconDiamond = baseUrl + "9/91/Season_2019_-_Diamond_1.png"
rankIconMaster = baseUrl + "1/11/Season_2019_-_Master_1.png"
rankIconGrandmaster = baseUrl + "7/76/Season_2019_-_Grandmaster_1.png"
rankIconChallenger = baseUrl + "5/5f/Season_2019_-_Challenger_1.png"


def GetRankIcon(rankStr):
    if rankStr:
        lowerCaseRank = rankStr.lower()
        if "iron" in lowerCaseRank:
            return rankIconIron
        elif "bronze" in lowerCaseRank:
            return rankIconBronze
        elif "silver" in lowerCaseRank:
            return rankIconSilver
        elif "gold" in lowerCaseRank:
            return rankIconGold
        elif "platinum" in lowerCaseRank:
            return rankIconPlatinum
        elif "diamond" in lowerCaseRank:
            return rankIconDiamond
        elif "grand" in lowerCaseRank:
            return rankIconGrandmaster
        elif "master" in lowerCaseRank:
            return rankIconMaster
        elif "challenger" in lowerCaseRank:
            return rankIconChallenger
    else:
        return ""


async def UpdateEmbeds(postedEmbeds, embedList, playerList):
    for x in range(10):  # update embeds
        newEmbed = discord.Embed()
        name = playerList[x]._username
        fixedName = name.replace(' ', '+')
        linkToOpGG = "https://euw.op.gg/summoner/userName="+fixedName.lower()

        nameWithChamp = playerList[x]._champion+" - "+name

        if x < 5:
            newEmbed.color = 0xff0033
        else:
            newEmbed.color = 0x085eff

        if 'None' in playerList[x]._rank:
            rank = "UNRANKED"
        else:
            rank = playerList[x]._rank

        winRatioString = "WR "+str(get_win_ratio.GetWinRatioQuick(
            playerList[x]._username, playerList[x]._championId, api_static_data.lol_watcher))
        if 'None' in winRatioString:
            wrString = 'No games'
        else:
            wrString = winRatioString
        newEmbed.set_author(name=nameWithChamp, url=linkToOpGG,  icon_url=str(
            "http://ddragon.leagueoflegends.com/cdn/" + api_static_data.latest + "/img/champion/" + playerList[x]._champion + ".png"))
        newEmbed.set_footer(text=rank+" ("+str(wrString)+")", icon_url=str(
            GetRankIcon(playerList[x]._rank)))
        embedList.append(newEmbed)
        await postedEmbeds[x].edit(embed=newEmbed)


async def PostEmbeds(ctx, embedList):
    postedEmbeds = []
    for x in range(10):  # post embeds without winratios
        ebd = await ctx.channel.send(embed=embedList[x])
        postedEmbeds.append(ebd)
        if(x == 4):
            await ctx.channel.send("- VS -")
    return postedEmbeds


async def makeEmbeds(message, playerList):
    embedList = []

    for x in range(10):
        newEmbed = discord.Embed()

        if x < 5:
            newEmbed.color = 0xff0033
        else:
            newEmbed.color = 0x085eff

        name = playerList[x]._username
        fixedName = name.replace(' ', '+')
        linkToOpGG = "https://euw.op.gg/summoner/userName="+fixedName.lower()

        nameWithChamp = playerList[x]._champion+" - "+name

        if 'None' in playerList[x]._rank:
            rank = "UNRANKED"
        else:
            rank = playerList[x]._rank

        newEmbed.set_author(name=nameWithChamp, url=linkToOpGG,  icon_url=str(
            "http://ddragon.leagueoflegends.com/cdn/" + api_static_data.latest + "/img/champion/" + playerList[x]._champion + ".png"))
        newEmbed.set_footer(text=rank, icon_url=str(
            GetRankIcon(playerList[x]._rank)))
        embedList.append(newEmbed)

    print("embeds created")

    postedEmbeds = await PostEmbeds(message, embedList)

    print("embeds posted")

    await UpdateEmbeds(postedEmbeds, embedList, playerList)


# global readable match data
matchGlobal = api.ApiResponse(None, 0, api.ResType.NULL)


async def GetSummoner(summonerName):
    summoner = api.GetPlayer(summonerName)

    if summoner.response == api.ResType.WAIT:
        time.sleep(summoner.waitTime+1)
        summoner = api.GetPlayer(summonerName)

    if(summoner.response == api.ResType.NODATA):
        return summoner

    elif(summoner.response == api.ResType.SUCCESS):
        return summoner


async def SetTeams(summonerName):
    summoner = api.GetPlayer(summonerName)
    if summoner.response == api.ResType.WAIT:
        time.sleep(summoner.waitTime)
        summoner = api.GetPlayer(summonerName)

    if(summoner.response == api.ResType.SUCCESS):
        match = api.GetMatch(summoner.data['id'])
        if match.response == api.ResType.WAIT:
            time.sleep(match.waitTime)
            match = api.GetMatch(summoner.data['id'])

        elif(match.response == api.ResType.SUCCESS):
            participantList = match.data['participants']
            playerList = []
            for players in participantList:
                playerTemp = {'summonerName': players['summonerName'],
                              'summonerId': players['summonerId'], 'championId': players['championId']}
                player = get_summoner.GetPlayer(playerTemp)
                playerList.append(player)

            match.data = playerList
            return match

        elif(match.response == api.ResType.NODATA):
            return match

    elif(summoner.response == api.ResType.NODATA):
        return summoner
